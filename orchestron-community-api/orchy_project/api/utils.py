import os
from django.conf import settings
from django.db.models import Q, F, Count, Aggregate, CharField, IntegerField, DateField, Func, Max, Value as V
from django.db.models.functions import Concat, Cast
import lxml.etree as xml
import uuid
import json
import sys
from api.app_log import *
from api.models import Vulnerability, User
from collections import Counter
from datetime import date as ddate
from functools import reduce
from parsers.exceptions import MalFormedXMLException
from django.forms.models import model_to_dict
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import codecs
import socket

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'


def draw_thumnail(text, temp_file):
    split_text = text.strip().split(' ')[:2]
    draw_text = ''.join([s[0].upper() for s in split_text if s and s.isalnum()])
    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    image = Image.new('RGBA', (150, 150),color = color)
    draw = ImageDraw.Draw(image)
    bounding_box = [50, 50, 100, 100]
    x1, y1, x2, y2 = bounding_box
    font_file = os.path.join(settings.FONT_ROOT,'arial.ttf')
    font = ImageFont.truetype(font_file, size=58)
    w, h = draw.textsize(draw_text, font=font)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    rad = 20
    draw.text((x, y), draw_text, align='center', font=font)
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=color)
    alpha = Image.new('L', image.size, color)
    w, h = image.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    image.putalpha(alpha)
    image.save(temp_file)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'superuser': user.is_superuser,
        'admin': user.is_admin,
        'username':user.username,
        'email':user.email,
        'org':user.org_id
    }


def get_single_vul_context(vuls):
    context = {}
    for v in vuls:
        cwe = v.cwe
        if context.get(cwe) is None:
            all_vuls = Vulnerability.objects.filter(scan__application=v.scan.application,cwe=cwe,is_false_positive=True)
            context[cwe] = {}
            context[cwe]['names'] = set()
            context[cwe]['tools'] = set()
            context[cwe]['potential_false_positive'] = all_vuls.exists()
            context[cwe]['evidences'] = {}
        context[cwe]['cwe'] = v.cwe
        context[cwe]['open_for'] = v.open_for
        context[cwe]['bug_id'] = v.jira_id
        context[cwe]['bug_status'] = v.jira_issue_status
        context[cwe]['sev'] = v.severity
        context[cwe]['is_false_positive'] = v.is_false_positive
        context[cwe]['owasp'] = v.owasp
        context[cwe]['tools'].add(v.tool)
        context[cwe]['names'].add((v.name,v.scan.application.name))
        context[cwe]['cvss'] = v.cvss
        context[cwe]['app_languages'] = v.scan.application.platform_tags
        org_obj = v.scan.application.org
        vul_info = {}
        context[cwe]['dread'] = vul_info.get('dread_score',0)
        context[cwe]['common_name'] = vul_info.get('name','')
        context[cwe]['description'] = vul_info.get('description','')
        context[cwe]['impact'] = vul_info.get('risk',{})
        context[cwe]['time_intro'] = vul_info.get('intro_time',{})
        context[cwe]['languages'] = vul_info.get('languages',[])
        context[cwe]['affected_users'] = vul_info.get('affected_users','')
        context[cwe]['damage'] = vul_info.get('damage','')
        context[cwe]['discoverability'] = vul_info.get('discoverability','')
        context[cwe]['exploitability'] = vul_info.get('exploitability','')
        context[cwe]['reproducibility'] = vul_info.get('reproducibility','')
        context[cwe]['app_url'] = v.scan.application.url 
        context[cwe]['app_id'] = v.scan.application.id  
        for evidence in v.vulnerabilityevidence_set.all():
            if context[cwe]['evidences'].get(evidence.url) is None:
                present = False
                if evidence.request or evidence.response or evidence.log:
                    present = True
                context[cwe]['evidences'][evidence.url] = {
                    'params':set(),
                    'req_res_present':present
                }
            context[cwe]['evidences'][evidence.url]['params'].add(evidence.param)
    return context


def get_request_response(host,evidences):
    domain = 'http://{0}'.format(host)
    context = {}
    for evidence in evidences:
        context[evidence.url] = {}
        if evidence.log:
            context[evidence.url]['log'] = '{0}/media/{1}'.format(domain,evidence.log)
        else:
            context[evidence.url]['request'] = '{0}/media/{1}'.format(domain,evidence.request)
            context[evidence.url]['response'] = '{0}/media/{1}'.format(domain,evidence.response)
        context[evidence.url]['owasp'] = evidence.vul.owasp
        context[evidence.url]['cwe'] = evidence.vul.cwe
        context[evidence.url]['scan_id'] = evidence.vul.scan.id
        context[evidence.url]['scan_name'] = evidence.vul.scan.name
        context[evidence.url]['scan_short_name'] = evidence.vul.scan.short_name
        context[evidence.url]['tool'] = evidence.vul.tool
        context[evidence.url]['app_url'] = evidence.vul.scan.application.url
        context[evidence.url]['app_name'] = evidence.vul.scan.application.name
        context[evidence.url]['app_id'] = evidence.vul.scan.application.id
    return context        


def get_closed_vul_context(host,vuls):
    context = {}
    domain = 'http://{0}'.format(host)
    for v in vuls:
        cwe = v.cwe
        if context.get(cwe) is None:
            all_vuls = Vulnerability.objects.filter(scan__application=v.scan.application,cwe=cwe,is_false_positive=True)
            context[cwe] = {}
            context[cwe]['names'] = set()
            context[cwe]['tools'] = set()
            context[cwe]['potential_false_positive'] = all_vuls.exists()
            context[cwe]['evidences'] = {}
        context[cwe]['cwe'] = v.cwe
        context[cwe]['open_for'] = v.open_for
        context[cwe]['bug_id'] = v.jira_id
        context[cwe]['bug_status'] = v.jira_issue_status
        context[cwe]['sev'] = v.severity
        context[cwe]['is_false_positive'] = v.is_false_positive
        context[cwe]['owasp'] = v.owasp
        context[cwe]['tools'].add(v.tool)
        context[cwe]['names'].add((v.name,v.scan.application.name))
        context[cwe]['cvss'] = v.cvss
        org_obj = v.scan.application.org
        vul_info = {}
        context[cwe]['dread'] = vul_info.get('dread_score',0)
        context[cwe]['common_name'] = vul_info.get('name','')
        context[cwe]['description'] = vul_info.get('description','')
        context[cwe]['impact'] = vul_info.get('risk',{})
        context[cwe]['time_intro'] = vul_info.get('intro_time',{})
        context[cwe]['languages'] = vul_info.get('languages',[])
        context[cwe]['affected_users'] = vul_info.get('affected_users','')
        context[cwe]['damage'] = vul_info.get('damage','')
        context[cwe]['discoverability'] = vul_info.get('discoverability','')
        context[cwe]['exploitability'] = vul_info.get('exploitability','')
        context[cwe]['reproducibility'] = vul_info.get('reproducibility','')
        context[cwe]['app_url'] = v.scan.application.url 
        context[cwe]['app_id'] = v.scan.application.id
        for evidence in v.vulnerabilityevidence_set.all():
            if context[cwe]['evidences'].get(evidence.url) is None:
                context[cwe]['evidences'][evidence.url] = set()
            context[cwe]['evidences'][evidence.url].add(evidence.param)
        remediation = v.vulnerabilityremediation_set.last()
        if remediation:
            user = User.objects.filter(id=remediation.remediated_by).last()
            if user:
                username = user.email
            else:
                username = ''
            context[cwe]['remediation'] = {
                'description':remediation.description,
                'file':'{0}/media/{1}'.format(domain,remediation.file),
                'remediated_by':username,
                'remediated_on':remediation.remediated_on
            }
    return context
        
    

def get_grade(vuls):
    return int(float(max([v['cvss'] for k,v in vuls.items()] or [0])) * (10.0))                        
 

def get_severity_by_name(name):
    sev_dict = {'high':3,'medium':2,'low':1,'info':0}
    return sev_dict.get(name,0)


def get_severity_by_num(num):
    sev_dict = {3:'high',2:'medium',1:'low',0:'info'}
    return sev_dict.get(num,0)


def get_severity(cvss):
    cvss = float(cvss)
    if cvss <= 10 and cvss >= 7.0:
        severity = 3
    elif cvss <= 6.9 and cvss >= 4.0:
        severity = 2
    elif cvss < 3.9 and cvss >= 0.1:
        severity = 1
    else:
        severity = 0
    return severity


def write_results(data):
    from api.false_positive_reduction import write_results_to_db
    """
    Writes the false positive reduction analysis data th ES (sarpaastra index)
    """
    write_results_to_db(data)


def log_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if settings.DEBUG:
        print("Line no :%s Exception %s"%(exc_traceback.tb_lineno,e))
    else:
        return exc_traceback.tb_lineno,e


def remove_file(file_name):
    """
    Removes a file of file_name which exists in the OS path
    """
    if os.path.exists(file_name):
        os.unlink(file_name)


def validate_allowed_files(flat_file):
    """
    Parse the xml and verify whether the xml header is under the valid uploadable xml files list
    """
    try:
        ext = flat_file.split('.')[-1]
        if ext == 'json':
            with codecs.open(flat_file,encoding='utf-8') as data_file:
                data = json.load(data_file)           
                is_zap_json = False
                is_burp = False
                is_bandit = False
                is_nodejs_json = False
                is_npm_audit_json = False
                if isinstance(data,dict):
                    print("yes yes yes")
                    is_zap_json = data.get('Report',[])
                    is_bandit = data.get('results',[])
                    is_nodejs_json = data.get('files',[])
                    is_npm_audit_json = data.get('advisories',{})
                if isinstance(data,list):
                    if data[0].get('issue',False):
                        is_burp = True
                        return 'Burp'
                if is_zap_json:
                    return 'ZAP'
                elif is_bandit:
                    return 'Bandit'
                elif is_nodejs_json:
                    return 'NodeJsScan'
                elif is_npm_audit_json:
                    return 'NpmAudit'
                else:
                    return None
        elif ext == 'xml':
            try:
                nreport = xml.parse(flat_file)
                root_elem = nreport.getroot()
                if root_elem is not None:
                    tag = root_elem.tag
                    nsmap = root_elem.nsmap.get(None)
                    if nsmap:
                        tag = tag.replace('{'+nsmap+'}','')
                    header = settings.HEADER_MAP.get(tag)
                    if header:
                        return header
                    else:
                        remove_file(flat_file)
                return None
            except (xml.XMLSyntaxError,xml.ParserError):
                return None
        else:
            return None
    except BaseException as e:
        log_exception(e)
        return None


def validate_flat_file(file_name):
    """
    Check whether the uploaded file has the extension ".xml" 
    """
    file_root, file_ext = os.path.splitext(file_name)
    if file_ext in ['.xml','.json']:        
        return True
    return False


def unique_file_path(file_name):
    """
    Returns a unique file path such that there is no ambiguity in file names
    """    
    file_root, file_ext = os.path.splitext(file_name)    
    uniq_name = "%s%s" % (uuid.uuid4(), file_ext)
    return uniq_name