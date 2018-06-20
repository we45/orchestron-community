from django.utils import timezone
import lxml.etree as xml
from os import path
import re
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 

sev_dict = {
	'4-High':3,
	'3-Medium':2,
	'2-Low':1,
	'1-Informational':0,
	'0-Safe':0,
}

def parse_appspider(xml_file,user_name,init_es):
	"""
	parses the xml file obtained by app spider and pushes the result 
	to results to DB
	"""
	try:
		print('appspider XML parsing initiated')               
		try:
			nreport = xml.parse(xml_file)   
		except (xml.XMLSyntaxError,xml.ParserError):
			raise MalFormedXMLException(user_name)
		root_elem = nreport.getroot() 
		path = r'VulnList/Vuln/VulnType'
		uniq_objs = root_elem.xpath(path)			
		vuls = set([i.text for i in uniq_objs])
		p = 'VulnList/Vuln/VulnType[text() = $name]'
		for v in vuls:
			obj = root_elem.xpath(p,name=v)  
			url_param_list = []
			for u in obj:
				parent_obj = u.getparent()
				url_param_list.append({
					'url':parent_obj.findtext('Url',default=''),
					'name':parent_obj.findtext('VulnParamType',default=''),
					'request':parent_obj.findtext('CrawlTraffic',default=''),
					'response':parent_obj.findtext('CrawlTrafficResponse',default=''),
				})			
			vul_name = re.sub('<[^<]+?>', '',parent_obj.findtext('VulnType',default=''))
			desc = re.sub('<[^<]+?>', '',parent_obj.findtext('Description',default=''))
			recommendation = re.sub('<[^<]+?>', '',parent_obj.findtext('Recommendation',default=''))
			cwe = parent_obj.findtext('CweId',default='0')
			severity = sev_dict.get(parent_obj.findtext('AttackScore',default=''),0)
			vul_dict = init_es	
			vul_dict['vulnerability'] = {
				'name':vul_name,
				'is_false_positive':False,
				'is_remediated':False,
				'is_deleted':False,
				'tool':'AppSpider',
				'confidence':2,
				'severity':severity,
				'description':desc,
				'remediation':recommendation,                
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

# parse_appspider('/Users/sharath/Documents/VulnerabilitiesSummary.xml','',{})		

