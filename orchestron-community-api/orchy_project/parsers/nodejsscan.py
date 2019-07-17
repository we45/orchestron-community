# import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from django.utils import timezone
import json
import inspect

def parse_nodejsscan(json_file,user_name,init_es):
	try:
		print('NodeJSScan parsing initiated')
		with open(json_file,'r',encoding='utf-8') as fp:
			results = json.load(fp)
			default_dict = {}
			for k, v in results.get('sec_issues').items():
				for x in v:
					default_dict[(x.get('title'))] = {'description': '', 'evidences': []}
					for z in v:
						d = {
							'url': z.get('path') +" line number "+str(z.get('line')),
							'param': z.get('filename'),
							'log': z.get('lines')
						}
						default_dict[(x.get('title'))]['evidences'].append(d)
						default_dict[(x.get('title'))]['description'] = z.get('description')
			for k,v in default_dict.items():
				vul_dict = init_es
				vul_dict['vulnerability'] = {
					'name': k,
					'is_false_positive':False,
					'is_remediated':False,
					'is_deleted':False,
					'tool':'NodeJsScan',
					'confidence':2,
					'severity':2,
					'description':v.get('description', ''),
					'remediation':'',
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'evidences':v.get('evidences', [])
				}
				write_results(vul_dict)
	except BaseException as e:
		log_exception(e)
	else:
		print('NodeJSScan parsing completed')
