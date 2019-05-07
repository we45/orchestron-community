import re
import json
import lxml.etree as xml
from os import path
from django.utils import timezone
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 
import sys
from base64 import b64encode
import os

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'burp_db.json')
cwe_dict = json.load(open(file_path,'r'))

def parse_burp(xml_file,user_name,init_es):
    """
        Parsing a given xml file using burp. This function returns a dictionary of scan parameters and
        update the ES.
    """    
    try:
        print('Burp XML parsing initiated')
        try:
            nreport = xml.parse(xml_file)
        except (xml.XMLSyntaxError,xml.ParserError):
            raise MalFormedXMLException(user_name)        
        root_elem = nreport.getroot()
        reg_path = r'issue/name'
        uniq_objs = root_elem.xpath(reg_path)
        vuls = set([i.text for i in uniq_objs])
        p = '{0}[text() = $name]'.format(reg_path)
        severity_dict = {
            'Information':0,
            'Low':1,
            'Medium':2,
            'High':3
        }
        burp_confidence_dict = {
            "Certain":3,
            "Firm":2,
            "Tentative":1,
        }
        for v in vuls:
            obj = root_elem.xpath(p,name=v)
            url_param_list = []
            for u in obj:
                parent_obj = u.getparent()
                req = parent_obj.find('requestresponse/request')
                res = parent_obj.find('requestresponse/response')
                request = response = b64encode(b'')
                if req is not None:
                    is_base64_encoded = True if req.get('base64') == 'true' else False
                    if is_base64_encoded:
                        request = bytes(req.text.encode('utf-8'))
                    else:
                        request = b64encode(bytes(req.text.encode('utf-8')))
                if res is not None:
                    is_base64_encoded = True if res.get('base64') == 'true' else False
                    if is_base64_encoded:
                        response = bytes(res.text.encode('utf-8'))
                    else:
                        response = b64encode(bytes(res.text.encode('utf-8')))
                url = 'http:/%s'%(parent_obj.findtext('path',default=''))
                url_param_list.append({
                    'url':parent_obj.findtext('location',default=''),
                    'name':parent_obj.findtext('path',default=''),
                    'request':request,
                    'response':response,
                })
            vul_name = parent_obj.findtext('name',default='')
            severity = parent_obj.findtext('severity','')
            issue_type = parent_obj.findtext('type','8389632')
            if severity:
                severity = severity_dict.get(severity)
            cwe_present = cwe_dict.get(issue_type,[])
            cwe = 0
            if cwe_present:
                cwe = cwe_present[0]
            desc = parent_obj.findtext('issueBackground',default='')
            solution = parent_obj.findtext('remediationBackground',default='')
            observation = parent_obj.find('issueDetail')
            confidence = parent_obj.findtext('confidence',default='')
            if confidence:
                confidence = burp_confidence_dict.get(confidence)
            if observation is not None:
                s = '''You should manually examine the application behavior and attempt to identify any unusual input validation or other obstacles that may be in place.'''
                obs = observation.text.replace(s,'')
            else:
                obs = ''
            vul_dict = init_es
            vul_dict['vulnerability'] = {
                'name':re.sub('<[^<]+?>', '',vul_name),
                'is_false_positive':False,
                'is_remediated':False,
                'is_deleted':False,
                'tool':'Burp',
                'confidence':confidence,
                'severity':severity,
                'description':re.sub('<[^<]+?>', '',desc),
                'vul_type':'Insecure Coding',
                'remediation':re.sub('<[^<]+?>', '',solution),
                'observations':obs,
                'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            vul_dict['vulnerability']['evidences'] = url_param_list
            vul_dict['vulnerability']['cwe'] = {
                'cwe_id':cwe
            }            
            write_results(vul_dict)
    except BaseException as e:
        log_exception(e)
    else:
        print('Checkmarx XML parsing completed')


# End-Of-File            