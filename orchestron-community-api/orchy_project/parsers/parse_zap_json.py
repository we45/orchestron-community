import json
import re
from django.utils import timezone
from api.utils import log_exception
from api.utils import write_results
from base64 import b64encode
import codecs

def parse_zap_json(file_path, user_name, init_es):
	try:
		with codecs.open(file_path,'r',encoding='utf-8') as fp:
			data = json.loads(fp.read())
			hosts = data.get('Report',{}).get('Sites',[])

			def post_results(hosts):
				host_url = hosts.get('Host','')
				alerts = hosts.get('Alerts',{})
				alert_items = alerts.get('AlertItem',[])

				def process_alerts(alert):
					severity = alert.get('RiskCode',0)
					desc = alert.get('Desc','')
					vul_name = alert.get('Alert','')
					solution = alert.get('Solution','')
					cwe = alert.get('CWEID',0)
					url_param_list = []
					items = alert.get('Item',[])
					if isinstance(items, list):
						for item in items:
							request = response = ''
							response_header = item.get('ResponseHeader','')
							response_body = item.get('ResponseBody','')
							if response_header or response_body:
								response = '{0}\n\n{1}'.format(response_header.encode('utf-8'),response_body.encode('utf-8'))
							request_header = item.get('RequestHeader','')
							request_body = item.get('RequestBody','')
							if request_header or request_body:
								request = '{0}\n\n{1}'.format(request_header.encode('utf-8'),request_body.encode('utf-8'))
							attack = item.get('Attack','')
							uri = item.get('URI','')							
							param = item.get('Param','')
							url = uri.split(':')[-1]
							evid_dict = {
								'url':url,
								'name':param,
								'attack':attack,
								'request':b64encode(bytes(request.encode('utf-8'))),
								'response':b64encode(bytes(response.encode('utf-8'))),
							}
							url_param_list.append(evid_dict)
					elif isinstance(items, dict):
						request = response = ''
						response_header = items.get('ResponseHeader','')
						response_body = items.get('ResponseBody','')
						if response_header or response_body:
							response = '{0}\n\n{1}'.format(response_header.encode('utf-8'),response_body.encode('utf-8'))
						request_header = items.get('RequestHeader','')
						request_body = items.get('RequestBody','')
						if request_header or request_body:
							request = '{0}\n\n{1}'.format(request_header.encode('utf-8'),request_body.encode('utf-8'))
						param = items.get('Attack','')
						uri = items.get('URI','')
						if not param:
							param = items.get('Param','')
						url = uri.split(':')[-1]
						evid_dict = {
							'url':url,
							'name':param,
							'request':b64encode(bytes(request.encode('utf-8'))),
							'response':b64encode(bytes(response.encode('utf-8'))),
						}
						url_param_list.append(evid_dict)
					vul_dict = init_es			
					vul_dict['vulnerability'] = {
						'name':re.sub('<[^<]+?>', '',vul_name),
						'is_false_positive':False,
						'is_remediated':False,
						'is_deleted':False,
						'tool':'ZAP',
						'confidence':2,
						'severity':severity,
						'description':re.sub('<[^<]+?>', '',desc),
						'vul_type':'Insecure Coding',
						'remediation':re.sub('<[^<]+?>', '',solution),                
						'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S") 
					}
					vul_dict['vulnerability']['evidences'] = url_param_list		
					vul_dict['vulnerability']['cwe'] = {
						'cwe_id':cwe,
						'cwe_link':'https://cwe.mitre.org/data/definitions/%s.html'%cwe
					}	
					write_results(vul_dict)

				if isinstance(alert_items,list):
					for alert in alert_items:
						process_alerts(alert)
				elif isinstance(alert_items,dict):
					process_alerts(alert_items)

			if isinstance(hosts,dict):
				post_results(hosts)
			elif isinstance(hosts,list):
				for host in hosts:
					post_results(host)

	except BaseException as e:
		log_exception(e)
	else: 
		print('XML Parsing Completed')



# parse_zap_json(file_path,init_es)		