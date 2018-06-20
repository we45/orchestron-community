from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 

def parse_checkmarx(xml_file,user_name,init_es):
	"""
	parses the xml file obtained by checkmarks scan and pushes the result 
	to results to DB
	"""
	try:
		print('Checkmarx XML parsing initiated')
		try:
			nreport = xml.parse(xml_file)   
		except (xml.XMLSyntaxError,xml.ParserError):
			raise MalFormedXMLException(user_name)
		root_elem = nreport.getroot()         
		queries = root_elem.findall("Query") 
		for q in queries:
			cwe = q.get('cweId',0)
			vul_name = q.get('name','Unknown')
			severity = q.get('SeverityIndex',0)
			language = q.get('Language','Unknown')
			results = q.findall('Result')
			url_param_list = []
			for r in results:
				nodes = r.findall('Path/PathNode')
				for n in nodes:
					filename = n.findtext('FileName',default='')
					line_num = n.findtext('Line',default='')
					# col_num = n.findtext('Column',default='')
					parameter = n.findtext('Name',default='')
					code = n.findtext('Snippet/Line/Code',default='')
					evid_desc = "File :{0}, Line :{1}, Parameter :{2}".format(filename,line_num,parameter)
					url_param_list.append({
						'url':filename,
						'name':evid_desc,
						'log':bytes(code.encode('utf-8'))
					})
			vul_dict = init_es	
			vul_dict['vulnerability'] = {
				'name':vul_name,
				'is_false_positive':False,
				'is_remediated':False,
				'is_deleted':False,
				'tool':'Checkmarx',
				'confidence':2,
				'severity':severity,
				'description':'',
				'remediation':'',                
				'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
				'cwe':{
					'cwe_id':cwe,
					'cwe_link':'https://cwe.mitre.org/top25/index.html#CWE-%s'%cwe
				},
				'evidences':url_param_list
			}
			write_results(vul_dict)
	except BaseException as e:
		log_exception(e)         
	else:         
		print('XML Parsing Completed')

# xml_file = '/Users/sharath/Documents/CTF Test App.xml'
# parse_checkmarx(xml_file,'','')