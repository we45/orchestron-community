# from lxml import etree
import lxml.etree as xml
import json
from os import path
import re
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from django.utils import timezone
from random import randint 
import sys
import os

# data = xml.parse('webgoat_output_OWASP_2013.xml')

sev_dict = {
	"Low":1,
	"Medium":2,
	"High":3,
	"Critical":3,
}
def parse_hp_fortify(xml_file,user_name,init_es):
	try:
		nreport = xml.parse(xml_file)   
	except (xml.XMLSyntaxError,xml.ParserError):
		raise MalFormedXMLException(user_name)
	rootelement = nreport.getroot()
	outsidepath = rootelement.xpath(r'//GroupingSection')
	print("HP Fortify parsing initiated")
	Kingdom_list = []
	for path_value in outsidepath:
		meta_info = path_value.findall("MajorAttributeSummary/MetaInfo")
		if len(meta_info) > 2:
			explination = meta_info[1].findtext('Value')
			recommendations=  meta_info[2].findtext('Value')
		issue_path=path_value.findall("Issue")
		for issue in issue_path:
			name = issue.findtext('Kingdom')
			set_kingdom = set(Kingdom_list)
			k = name in set_kingdom
			Kingdom_list.append(name)
			friority = issue.findtext('Friority')
			if not k:
				evids = []
				for issue_list in issue_path:
					if name == issue_list.findtext('Kingdom'):
						s = issue_list.find("Primary")
						s2 = issue_list.find("Source")
						if s is not None:
							d = {
								'name':'File : {0} LineNum : {1}'.format(s.findtext('FileName',default='Unknown'),s.findtext('LineStart',default='Unknown')),
								'url':s.findtext('FilePath',default=''),
								'log':s.findtext('Snippet',default='')
							}
							evids.append(d)
						if s2 is not None:
							d1 = {
								'name':'File : {0} LineNum : {1}'.format(s2.findtext('FileName',default='Unknown'),s2.findtext('LineStart',default='Unknown')),
								'url':s2.findtext('FilePath',default=''),
								'log':s2.findtext('Snippet',default='')
							}
							evids.append(d1)
				vul_dict = init_es
				vul_dict['vulnerability'] ={
					'tool':'HP Fortify',
					'name': name,
					'is_false_positive':False,
					'is_remediated':False,
					'description': explination,
					'remediation': recommendations,
					'severity':sev_dict.get(friority,0),
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'evidences':evids
				}
				write_results(vul_dict)
	print("HP Fortify parsing completed")


# with io.open("testJson.json",'w',encoding="utf-8") as outfile:
#   outfile.write(unicode(json.dumps(d, ensure_ascii=False)))
