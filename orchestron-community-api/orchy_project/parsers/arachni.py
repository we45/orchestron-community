from django.utils import timezone
import lxml.etree as xml
from os import path
import re
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 
from collections import defaultdict
import json
from base64 import b64encode

sev_dict = {
	"informational":0,
	"low":1,
	"medium":2,
	"high":3,
}

def parse_arachni(json_file,user_name,init_es):
	"""
	parses the json file obtained by arachni scanner and pushes the result 
	to results to DB
	"""
	try:
		print('Arachni parsing initiated')  
		with open(json_file) as fp:
			data = json.load(fp)
			new_vuls = defaultdict(list)
			for detail in data.get('issues', []):
				name =  detail.get('name', '')
				cwe = detail.get('cwe', '')
				description = detail.get('description', '')
				severity = detail.get('severity', '')
				references = detail.get('references',{}).get('OWASP', '')
				remediation = detail.get('remedy_guidance', '')
				url = detail.get('vector', {}).get('url', '')
				parameter = detail.get('vector', {}).get('affected_input_name', '')
				response = detail.get('response', {}).get('headers', {})
				request = detail.get('request', {}).get('headers', {})
				req_str = res_str = ''
				for k,v in request.items():
					req_str += "\n{0} : {1}".format(k,v)
				for k,v in response.items():
					res_str += "\n{0} : {1}".format(k,v)
				new_vuls[(name,description,remediation,severity,cwe,references)].append({
					'url':url,
					'name':parameter,
					'request':b64encode(req_str),
					'response':b64encode(res_str)
				})	
			for d,url_param_list in new_vuls.items():
				vul_dict = init_es
				vul_dict['vulnerability'] = { 
					'name':d[0],
					'description':d[1],
					'is_false_positive':False,
					'is_remediated':False,
					'is_deleted':False,
					'tool':'Arachni',
					'severity':sev_dict.get(d[3],0),
					'description':'',
					'remediation':d[2],                
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'cwe':{
						'cwe_id':d[4]
					},
					'evidences':url_param_list
				}
				write_results(vul_dict)
	except BaseException as e:
		log_exception(e)         
	else:         
		print('Json Parsing Completed')

# parse_arachni('/Users/sharath/Documents/VulnerabilitiesSummary.xml','',{})		

