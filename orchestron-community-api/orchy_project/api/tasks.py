from background_task import background
import time
from django.utils import timezone
from datetime import datetime,timedelta
from parsers.burp import parse_burp
from parsers.zap import parse_zap
from parsers.parse_zap_json import parse_zap_json
from parsers.findsecbug import parser_findsecbug
from parsers.burp_json import parse_burp_json
from parsers.owasp_dep_checker import parse_owasp_dep_checker
from api.models import Scan, WebhookLog, Application, JiraIssueTypes, Vulnerability, \
    VulnerabilityEvidence, JiraUsers, ScanLog
from api.utils import remove_file,log_exception
from api.app_log import *
import io
from api.jira_utils import get_jira_con
from time import sleep
from api.orl import get_open_vul_info_from_api
from django.conf import settings
from api.models import User
from django.contrib.sites.models import Site
from base64 import b64encode

@background()
def sync_jira_users(org_id):
    print('Sync JIRA Users')
    jira_config = JiraIssueTypes.objects.get(org__id=org_id)
    jira_con = get_jira_con(jira_config)
    if jira_con:
        try:
            groups = jira_con.groups()
            for group in groups:
                try:
                    members = jira_con.group_members(group)
                    for member,member_dict in members.items():
                        if member_dict.get('active'):
                            ud = {
                                'name':member,
                                'group':group,
                                'jira_config':jira_config
                            }
                            exists,created = JiraUsers.objects.get_or_create(**ud)  
                except BaseException as e:
                    log_exception(e)
        except BaseException as e:
            log_exception(e)


@background()
def raise_jira_ticket(obj,org_id):
    """
    Raises the jira ticket on accurance of vul
    """
    try:
        app_id = obj.get('app_id','') 
        vul_name = obj.get('vul_name','')
        cwe = int(obj.get('cwe',0))
        project_key = obj.get('project_key','')
        issuetype = obj.get('issuetype','Bug')
        assignee = obj.get('assignee')
        app_obj = Application.objects.get(pk=app_id)
        if app_id and vul_name:
            vuls = Vulnerability.objects.filter(is_false_positive=False,is_remediated=False,scan__application=app_obj,cwe=cwe,name=vul_name)
            jira_obj = JiraIssueTypes.objects.get(org__id=org_id)
            jira = get_jira_con(jira_obj)  
            if jira and vuls.exists():                
                complete_desc = ''
                references = ''              
                if app_obj:
                    complete_desc += 'Application:\n{0}\n\n'.format(app_obj.name)
                    complete_desc += 'Application URL:\n{0}\n\n'.format(app_obj.url)
                if cwe:
                    complete_desc += 'CWE :\n{0}\n\n'.format(cwe)
                org_obj = app_obj.org
                if org_obj.orl_config_exists():
                    vul_info = get_open_vul_info_from_api(cwe,org_obj)
                    complete_desc += 'Description:\n{0}\n\n'.format(vul_info.get('description','')) 
                if references:
                    complete_desc += 'References:\n{0}'.format(references)                
                data_dict = {
                    'project':{'key':project_key },
                    'issuetype':{'name': issuetype},
                    'summary':vul_name,
                    'description':complete_desc,                
                }            
                new_issue = jira.create_issue(**data_dict) 
                evids = VulnerabilityEvidence.objects.filter(vul__in=vuls)                
                attachment = io.StringIO()
                attachment.write('Evidences')  
                for evid in evids:
                    data = '\n\t- {0}\n\t\t- {1}'.format(evid.url,evid.name)
                    attachment.write(data)   
                jira.add_attachment(issue=new_issue, attachment=attachment, filename='evidences.txt')                    
                vuls.update(jira_id=str(new_issue),jira_issue_status=str(new_issue.fields.status))
                info_debug_log(event='Raise Jira ticket',status='success')
                if assignee:
                    jira.assign_issue(new_issue,assignee)
                    info_debug_log(event='Assign Jira ticket to an assignee',status='success')
    except BaseException as e:
        print("Error raising JIRA tickets")
        # general_error_messages.delay(path='raise_jira_ticket function',msg=log_exception(e))
        critical_debug_log(event=e,status='failure')


def process_files(user, application, complete_path, init_es, tool, scan_name, user_host, to_name,hook_log=None):
    """
    calls the parsers to parse the xml file according to the tool selected
    """
    try:
        application = Application.objects.get(id=application)
        scan = Scan.objects.get(name=scan_name)
        scan.scanlog.status = 'Initiated'
        scan.scanlog.save()
        scan_log = scan.scanlog
        scan_log.status = 'In Progress'
        scan_log.save()
        try:
            if tool == 'Burp':            
                ext = complete_path.split('.')[-1]
                if ext == 'json':
                    parse_burp_json(complete_path,user,init_es)
                elif ext == 'xml':
                    parse_burp(complete_path,user,init_es)
            elif tool == 'ZAP':
                ext = complete_path.split('.')[-1]
                if ext == 'json':
                    parse_zap_json(complete_path,user,init_es)
                elif ext == 'xml':
                    parse_zap(complete_path,user,init_es)            
            elif tool == 'OWASP Dependency Checker':
                parse_owasp_dep_checker(complete_path,user,init_es)            
            elif tool == "FindSecBugs":
                parser_findsecbug(complete_path,user,init_es)                            
            info_debug_log(ip=user_host,user=user,event='XML Parsing',status='success')
            if hook_log:
                hook_log.scan_process_event = True
                hook_log.scan_process_exception = ''
                hook_log.scan_process_datetime = timezone.now()
                hook_log.scan_id = scan.name
                hook_log.vul_process_event = True
                hook_log.vul_process_exception = ''
                hook_log.vul_process_datetime = timezone.now()
                hook_log.save()
            scan_log.status = 'Completed'
            scan_log.save()
        except BaseException as e:
            scan_log.status = 'Killed'
            scan_log.save()
            scan.delete()
            log_exception(e)
            if hook_log:
                hook_log.vul_process_event = False
                hook_log.vul_process_exception = e
                hook_log.vul_process_datetime = timezone.now()
                hook_log.scan_process_event = False
                hook_log.scan_process_exception = e
                hook_log.scan_process_datetime = timezone.now()
                hook_log.scan_id = ''
                hook_log.save()
            # general_error_messages.delay(path='process_files function',msg=log_exception(e))
            critical_debug_log(ip=user_host,user=user,event=e,status='failure')
    except BaseException as e:
        log_exception(e)
        scan_log.status = 'Killed'
        scan_log.save()
        critical_debug_log(ip=user_host,user=user,event=e,status='failure')
        if hook_log:
            hook_log.scan_process_event = False
            hook_log.scan_process_exception = e
            hook_log.scan_process_datetime = timezone.now()
            hook_log.scan_id = ''
            hook_log.save()  
    finally:
        info_debug_log(ip=user_host,user=user,event='Remove file after XML parsing',status='success')
        remove_file(complete_path)


def process_json(user, application, json_dict, init_es, tool, scan_name, user_host, to_name,hook_log=None):
    """
    calls the parsers to parse the json dict
    """
    try:
        application = Application.objects.get(id=application)
        scan = Scan.objects.get(name=scan_name)
        try:
            tool = json_dict.get('tool','Unknown')
            vuls = json_dict.get('vulnerabilities',[])
            scan.tool = tool
            scan.save()
            for vul in vuls:
                vul_dict = init_es
                vul_dict['vulnerability'] = vul
                vul_dict['vulnerability']['tool'] = tool
                vul_dict['vulnerability']['cwe'] = {'cwe_id':vul.get('cwe',0)}
                write_results(vul_dict)
            info_debug_log(ip=user_host,user=user,event='JSON processing',status='success')
            if hook_log:
                hook_log.scan_process_event = True
                hook_log.scan_process_exception = ''
                hook_log.scan_process_datetime = timezone.now()
                hook_log.scan_id = scan.name
                hook_log.vul_process_event = True
                hook_log.vul_process_exception = ''
                hook_log.vul_process_datetime = timezone.now()
                hook_log.save()
        except BaseException as e:
            scan.delete()
            if hook_log:
                hook_log.vul_process_event = False
                hook_log.vul_process_exception = e
                hook_log.vul_process_datetime = timezone.now()
                hook_log.scan_process_event = False
                hook_log.scan_process_exception = e
                hook_log.scan_process_datetime = timezone.now()
                hook_log.scan_id = ''
                hook_log.save()
            # general_error_messages.delay(path='process_json function',msg=log_exception(e))
            critical_debug_log(user=user,event=e,status='failure')
    except BaseException as e:
        critical_debug_log(user=user,event=e,status='failure')
        if hook_log:
            hook_log.scan_process_event = False
            hook_log.scan_process_exception = e
            hook_log.scan_process_datetime = timezone.now()
            hook_log.scan_id = ''
            hook_log.save()  
    

@background()
def parse_xmls(user, application, complete_path, init_es, tool, scan_name, user_host, to_name):
    """
    calls the parsers to parse the xml file according to the tool selected
    """
    process_files(user, application, complete_path, init_es, tool, scan_name, user_host, to_name)
    info_debug_log(event='Parse xmls',status='success')


@background()
def webhook_upload(user, application, complete_path, init_es, tool, scan_name, user_host, to_name,hook_log):
    """
    webhook uploades the xml  files for parsing and saves the log by event handling
    """
    hook_log = WebhookLog.objects.get(id=hook_log)
    hook_log.file_upload_event = True
    hook_log.file_upload_datetime = timezone.now()
    hook_log.save()
    process_files(user, application, complete_path, init_es, tool, scan_name, user_host, to_name,hook_log=hook_log)
    info_debug_log(event='Webhook upload',status='success')


@background()
def webhook_process_json(user, application, json_dict, init_es, tool, scan_name, user_host, to_name,hook_log):
    """
    webhook processes the json for parsing and saves the log by event handling
    """
    hook_log = WebhookLog.objects.get(id=hook_log)
    hook_log.file_upload_event = True
    hook_log.file_upload_datetime = timezone.now()
    hook_log.save()
    process_json(user, application, json_dict, init_es, tool, scan_name, user_host, to_name,hook_log=hook_log)
    info_debug_log(event='Webhooks - json process',status='success')




from django.core.mail import EmailMultiAlternatives, EmailMessage,get_connection
from django.contrib.auth.tokens import default_token_generator    
from django.template import loader

def make_token(user):
    token = default_token_generator.make_token(user)
    return token

@background()
def forgot_email_reset(email,subject,domain_override,email_template_name,use_https, protocol_type):
    try:
        user = User.objects.get(email=email)
        if user:
            email_certs = 'TLS'
            EMAIL_HOST_TYPE = 'SMTP'
            EMAIL_HOST = settings.EMAIL_HOST
            EMAIL_PORT = settings.EMAIL_PORT
            EMAIL_HOST_USER = settings.EMAIL_HOST_USER
            EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
            from_email = settings.FROM_EMAIL
            EMAIL_USE_TLS = True
            display_email = 'Orchestron'
            if EMAIL_HOST_TYPE == 'SMTP':
                USE_TLS = email_certs != 'SSL'
                USE_SSL = email_certs == 'SSL'
                connection = get_connection(host=EMAIL_HOST,port=EMAIL_PORT,username=EMAIL_HOST_USER,password=EMAIL_HOST_PASSWORD,
                    use_tls=EMAIL_USE_TLS, fail_silently=False,timeout=None)
                connection.open()
                from_full_email = '{0} <{1}>'.format(display_email,from_email)
                if domain_override is None:
                    current_site = Site.objects.get_current()
                    site_name = current_site.name
                    domain = current_site.domain
                else:
                    site_name = domain = domain_override
                from django.core.mail import send_mail
                t = loader.get_template(email_template_name)
                c = {
                    'email': user.email,
                    'name':user.username,
                    'domain': protocol_type+'://'+domain,
                    'site_name': site_name,
                    'uid': str(b64encode(bytes(str(user.id).encode('utf-8'))),'utf-8'),
                    'user': user,
                    'token': make_token(user),
                    'protocol': use_https and 'https' or 'http'
                }
                email = EmailMultiAlternatives(subject, '', from_full_email, [user.email],connection=connection)
                email.attach_alternative(t.render(c), "text/html")
                email.send()
                connection.close()
    except Exception as e:
        critical_debug_log(user=user,event=e,status='failure')
      