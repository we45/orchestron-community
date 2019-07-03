# import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from django.utils import timezone
import json
import inspect

def parse_npm_audit(json_file,user_name,init_es):
	try:
		with open(json_file, 'r',encoding='utf-8') as fp:
			results = json.load(fp)
			severity_dict = {"critical":3,"high":2,"moderate":1,"	":0,"info":0}
			advisories = results.get('advisories')
			for vul in advisories.values():
				name = vul.get('title','')
				desc = vul.get('overview','')
				recommendation = vul.get('recommendation','')
				module_name = vul.get('module_name','')
				cves = vul.get('cves',[])
				cve = ''
				if cves:
					cve = cves[0]
				severity = int(severity_dict.get(vul.get('severity'),0))
				cwe_string = vul.get('cwe',"").replace('CWE-','') or 0
				cwe = int(cwe_string)
				evid_list = []
				findings = vul.get('findings',[])
				for f in findings:
					version = f.get('version','')
					dep_dict = {
						'file_paths':[]
					}
					paths = f.get('paths',[])
					for p in paths:
						dep_dict['file_paths'].append(p)
					data_dict = {
						'module':module_name,
						'version':version,
						'related_dependency':dep_dict,
						'cve':cve
					}
					evid_list.append(data_dict)
				vul_dict = init_es
				vul_dict['vulnerability'] = {
					'name': name,
					'is_false_positive':False,
					'is_remediated':False,
					'tool':'NpmAudit',
					'confidence':2,
					'severity':severity,
					'description':desc,
					'remediation':recommendation,
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'evidences':evid_list
				}
				if cwe:
					vul_dict['vulnerability']['cwe'] = {
						'cwe_id':cwe,
						'cwe_link':'https://cwe.mitre.org/data/definitions/%s.html'%cwe
					}
				write_results(vul_dict)
	except BaseException as e:
		log_exception(e,module_name=inspect.stack()[0][3])
	else:
		print('NPM Audit parsing completed')
