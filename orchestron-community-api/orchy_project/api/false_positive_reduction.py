from django.utils import timezone
from api.utils import log_exception,get_severity
from django.conf import settings
from api.models import Vulnerability,Scan,VulnerabilityEvidence,Application,JiraConfigurations
from uuid import uuid4
from datetime import datetime
import os
import json
from api.app_log import *
from api.orl import get_open_vul_info_from_api, get_open_vul_name_from_api, get_cwe_from_name
from api.minio_utils import MinioUtil


def create_vul(data,es_reference,confidence,severity,cwe,tool,evidences):
    try:
        evid_dir_path = settings.EVIDENCE_ROOT
        if not os.path.isdir(evid_dir_path):
            os.mkdir(evid_dir_path)
        cvss_dict = {3:7.5,2:4.5,1:2.5,0:0}
        vul_name = data['vulnerability'].get('name','')
        created_on = timezone.now()
        # created_on = data['vulnerability'].get('created_on',timezone.now())
        scan_obj = Scan.objects.select_related('application__org').get(name=es_reference)
        org_obj = scan_obj.application.org
        cwe = cwe or 0
        if org_obj.orl_config_exists():
            common_name = get_open_vul_name_from_api(cwe,org_obj)
            vul_info = get_open_vul_info_from_api(cwe,org_obj)
            dread_score = vul_info.get('dread_score',0)
        else:
            common_name = vul_name[:255]
            dread_score = 0
        if severity == 4 or severity == '4':
            severity = 3
        try:
            meta_dict = {
                'name':vul_name[:255],
                'description':data['vulnerability'].get('description','N/A'),
                'remediation':data['vulnerability'].get('remediation','N/A'),
                'tool':tool,
                'is_false_positive':data['vulnerability'].get('is_false_positive',False),
                'is_remediated':data['vulnerability'].get('is_remediated',False),
                'confidence':int(confidence),
                'severity':int(severity),
                'vul_type':data['vulnerability'].get('vul_type','Configuration'),
                'owasp':data['vulnerability'].get('owasp','Uncategorized'),
                'cvss':data['vulnerability'].get('cvss',cvss_dict.get(severity)),
                'cwe':int(cwe),
                'scan':scan_obj,
                'dread':dread_score,
                'common_name':common_name
            }
            vul = Vulnerability.objects.create(**meta_dict)
            vul.created_on = created_on
            vul.edited_on = created_on
            vul.save()
            evids = []
            for evid in evidences:
                log = evid.get('log','')
                request_file_name = ''
                response_file_name = ''
                log_file_name = ''
                if log:
                    log_file_name = '{0}log_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
                    full_path = os.path.join(settings.MEDIA_ROOT,log_file_name)
                    with open(full_path,'wb') as fp:
                        if not isinstance(log,bytes):
                            log = bytes(log.encode('utf-8'))
                        fp.write(log)
                    MinioUtil().upload_file_from_path(log_file_name,full_path)
                else:
                    request = evid.get('request','')
                    response = evid.get('response','')
                    if request:
                        request_file_name = '{0}request_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
                        full_path = os.path.join(settings.MEDIA_ROOT,request_file_name)
                        with open(full_path,'wb') as fp:
                            if not isinstance(request,bytes):
                                request = bytes(request.encode('utf-8'))
                            fp.write(request)
                        MinioUtil().upload_file_from_path(request_file_name,full_path)
                    if response:
                        response_file_name = '{0}response_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
                        full_path = os.path.join(settings.MEDIA_ROOT,response_file_name)
                        with open(full_path,'wb') as fp:
                            if not isinstance(response,bytes):
                                response = bytes(response.encode('utf-8'))
                            fp.write(response)
                        MinioUtil().upload_file_from_path(response_file_name,full_path)
                data = {
                    'vul':vul,
                    'url':evid.get('url',''),
                    'param':evid.get('name',''),
                    'request':request_file_name,
                    'response':response_file_name,
                    'log':log_file_name
                }
                evids.append(VulnerabilityEvidence(**data))
            if evids:
                VulnerabilityEvidence.objects.bulk_create(evids)
                info_debug_log(event='Bulk-create vulnerability',status='success')
        except Scan.DoesNotExist:
            pass
    except BaseException as e:
        log_exception(e)
        # general_error_messages.delay(path='create_vul function',msg=log_exception(e))
        critical_debug_log(event=e,status='failure')



def write_results_to_db(data):
    """
        This function processes the vulnerabilities identified by the scanner to identify and
        reduce the false positives. 
    """
    try:
        vul_name = str(data.get('vulnerability',{}).get('name',''))

        severity_dict = {4:3,3:3,2:2,1:1,0:0}   
        cvss_dict = {3:7.5,2:4.5,1:2.5,0:0}     

        if vul_name:
            app_name = data.get('host',{}).get('name')
            app_obj = Application.objects.get(name=app_name)
            tool = data.get('vulnerability',{}).get('tool')        

            severity = data.get('vulnerability',{}).get('severity')
            if severity:
                severity = severity_dict.get(int(severity))

            cwe_id = data.get('vulnerability',{}).get('cwe',{}).get('cwe_id',0)          

            confidence = int(data.get('vulnerability',{}).get('confidence',2))           


            burp_confidence_dict = {
                "Certain":3,
                "Firm":2,
                "Tentative":1,
            } 
            zap_confidence_dict = {
                "Medium":2,
                "Low":1                
            } 
            data['vulnerability']['vul_type'] = data['vulnerability'].get('vul_type','Configuration')
            data['vulnerability']['owasp'] = data['vulnerability'].get('owasp','Uncategorized')
            data['vulnerability']['cvss'] = data['vulnerability'].get('cvss',cvss_dict.get(severity))
            data['vulnerability']['cwe'] = {
                'cwe_id': cwe_id   
            }
            if tool == 'Burp':
                if confidence == 3:
                    data['vulnerability']['is_false_positive'] = False
                elif confidence == 2:
                    data['vulnerability']['is_false_positive'] = False
                elif confidence == 1:
                    data['vulnerability']['is_false_positive'] = True
            elif tool == 'ZAP':
                if confidence == 1:
                    data['vulnerability']['is_false_positive'] = True
                elif confidence == 2:
                    data['vulnerability']['is_false_positive'] = False
            vuls = Vulnerability.objects.select_related('vul','scan__application').filter(name=vul_name,tool=tool,is_false_positive=True,scan__application__name=app_name)     
            if vuls.exists():
                data['vulnerability']['is_false_positive'] = True
                
            cwe = str(data['vulnerability'].get('cwe',{}).get('cwe_id',0))
            es_reference = data.get('scan_reference',{}).get('es_reference','')
            if not cwe:
                scan_obj = Scan.objects.select_related('application__org').get(name=es_reference)
                org_obj = scan_obj.application.org
                if org_obj.orl_config_exists():
                    cwe = get_cwe_from_name(vul_name,org_obj)
                    data['vulnerability']['cwe'] = {'cwe_id':cwe}                     
            if cwe:              
                data['vulnerability']['cwe']['cwe_id'] = cwe
                data['vulnerability']['severity'] = severity                                                               
            else:
                if severity == 0 or severity == 1:
                    if severity == 0:
                        cvss = 0
                    else:
                        cvss = 2
                    data['vulnerability']['vul_type'] = 'Configuration'
                    data['vulnerability']['owasp'] = 'Security Misconfiguration'
                    data['vulnerability']['cvss'] = cvss
                    data['vulnerability']['cwe']['cwe_id'] = 0
            data['vulnerability']['name'] = vul_name 
            evidences = data.get('vulnerability',{}).get('evidences',[])
            create_vul(data,es_reference,confidence,severity,cwe,tool,evidences)
            info_debug_log(event='Write false positive data to ES',status='success')
    except BaseException as e:
        log_exception(e)
        critical_debug_log(event=e,status='failure')
        # general_error_messages.delay(path='write_fpdata_to_es function',msg=log_exception(e))