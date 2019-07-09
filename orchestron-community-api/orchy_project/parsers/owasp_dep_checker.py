from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from bs4 import BeautifulSoup
from django.utils import timezone
from dateutil import parser
import inspect
import re
import lxml.etree as xml

def parse_owasp_dep_checker(xml_file,user_name,init_es):
	"""
	parses the xml file obtained by OWASP dependency checker and pushes the result 
	to results to DB
	"""
	try:
		nreport = xml.parse(xml_file)
		root_elem = nreport.getroot()
		NS = "{%s}"%root_elem.nsmap.get(None)
		projectInfo = root_elem.find('%sprojectInfo'%NS)
		if projectInfo is not None:
			scan_date = projectInfo.findtext('%sreportDate'%NS,default='')
			created_on = parser.parse(scan_date).strftime("%Y-%m-%d %H:%M:%S")
		dependencies = root_elem.findall('%sdependencies/%sdependency'%(NS,NS))
		severity_dict = {
			'Low': 1,
			'Medium': 2,
			'High': 3,
			'Information': 0,
			'Info': 0,
		}
		names_list = []
		vul_dict = {}
		for dependency in dependencies:
			url_param_list = []
			vulnerabilities_parent = dependency.find('%svulnerabilities'%NS)
			related_dependencies_parent = dependency.find('%srelatedDependencies'%NS)
			if vulnerabilities_parent is not None:
				evidence = dependency.findtext('%sevidence[@type="version"]/%sname'%(NS,NS))
				module = dependency.findtext('%sfileName'%NS,default='')
				version = dependency.findtext('%sevidenceCollected/%sevidence[@type="version"][@confidence="HIGHEST"]/%svalue'%(NS,NS,NS),default='')
				dep_dict = {
					'file_paths':[]
				}
				if related_dependencies_parent is not None:
					related_dependencies = related_dependencies_parent.findall('%srelatedDependency'%NS)
					for dep in related_dependencies:
						filePath = dep.findtext('%sfilePath'%NS,default='')
						dep_dict['file_paths'].append(filePath)
				vulnerabilities = vulnerabilities_parent.findall('%svulnerability'%NS)
				for vuln in vulnerabilities:
					vul_name = vuln.findtext('%sname'%NS,default='')
					if vul_name not in vul_dict:
						vul_dict[vul_name] = {
							'evidences':[]
						}
					severity = severity_dict.get(vuln.findtext('%sseverity'%NS,default=''),'Low')
					description = vuln.findtext('%sdescription'%NS,default='')
					cwe = vuln.findtext('%scwe'%NS,default='')
					if cwe:
						match = re.search(r'(CWE-)(\d{1,9})(.*?)',cwe)
						if match:
							cwe = match.group(2)
					cve = ''
					match = re.search(r'(CVE)-(\d+)-(\d+)',vul_name)
					if match:
						cve = match.group()
					url_param_list.append({
						'url':module,
						'name':version,
						'log':''
						})
					data_dict = {
						'name':vul_name,
						'is_false_positive':False,
						'is_remediated':False,
						'tool':'OWASP Dependency Checker',
						'confidence':2,
						'severity':severity,
						'description':description,
						'remediation':'',
						'created_on':created_on,
						'cwe':{
							'cwe_id':cwe,
							'cwe_link':'https://cwe.mitre.org/data/definitions/{0}.html'.format(cwe)
						}
					}
					vul_dict[vul_name]['evidences'] = url_param_list
					vul_dict[vul_name].update(data_dict)
		for v in vul_dict.values():
			vul_dict_final = init_es
			vul_dict_final['vulnerability'] = v
			write_results(vul_dict_final)
	except BaseException as e:
		log_exception(e)
	else:
		print('[ + ] OWASP Dependency Checker parsing completed')