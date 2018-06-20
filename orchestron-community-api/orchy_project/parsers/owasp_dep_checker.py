from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from datetime import datetime
from bs4 import BeautifulSoup


def parse_owasp_dep_checker(xml_file,user_name,init_es):
	"""
	parses the xml file obtained by OWASP dependency checker and pushes the result 
	to results to DB
	"""
	try:
		file = open(xml_file).read()
		data = BeautifulSoup(file,'lxml')
		dependencies = data.findAll('dependencies')
		severity_dict = {
			'Low': 1,
			'Medium': 2,
			'High': 3,
			'Information': 0,
			'Info': 0,
			}
		for dependency in data.findAll('dependency'):
			vulnerabilities = dependency.find('vulnerabilities')
			url_param_list = []
			if vulnerabilities:
				filename = dependency.find('filename').get_text()
				evid_desc = dependency.find('filepath').get_text()
				vulnerability = dependency.findAll('vulnerability')
				for vuln in vulnerability:
					vul_name = vuln.find('name').get_text()
					description = vuln.find('description').get_text()
					severity = severity_dict.get(vuln.find('severity').get_text(),'Low')
					url_param_list.append({
						'url':filename,
						'name':evid_desc,
						'log':''
						})
					cwe = 0
					if vuln.find('cwe'):
						cwe = vuln.find('cwe').get_text().split(' ')[0].split('CWE-')[1]

					vul_dict = init_es
					vul_dict['vulnerability'] = {
						'name':vul_name,
						'is_false_positive':False,
						'is_remediated':False,
						'is_deleted':False,
						'tool':'Owasp Dependency Checker',
						'confidence':2,
						'severity':severity,
						'description':description,
						'remediation':'',
						'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
						'cwe':{
							'cwe_id':cwe,
							'cwe_link':'https://cwe.mitre.org/top25/index.html#CWE-{0}'.format(cwe)
							},
						'evidences': url_param_list
						}
					write_results(vul_dict)

	except BaseException as e:
		log_exception(e)