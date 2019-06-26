import lxml.etree as xml
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from api.utils import log_exception
import re
from dateutil import parser
from parsers.utils import get_created_on
import inspect

def parse_zap(xml_file,user_name,init_es):
	"""
	Parsing a given xml file using zap. This function returns a dictionary of scan parameters and
    update the ES.
	"""
	try:
		nreport = xml.parse(xml_file)
		root_elem = nreport.getroot()
		scan_date = root_elem.attrib.get('generated')
		created_on = get_created_on(scan_date)
		host_name = init_es.get('host',{}).get('app_uri')
		sites = root_elem.findall('site')
		for site in sites:
			host = site.get('name')
			path = r'alerts/alertitem/alert'
			uniq_objs = site.xpath(path)
			vuls = set([i.text for i in uniq_objs])
			p = 'alerts/alertitem/alert[text() = $name]'
			for v in vuls:
				obj = site.xpath(p,name=v)
				url_param_list = []
				for u in obj:
					parent_obj = u.getparent()
					instances = parent_obj.find('instances')
					if instances is not None:
						instance_list = instances.findall('instance')
						for ins in instance_list:
							url_param_list.append({'url':ins.findtext('uri',default=''),'param':ins.findtext('param',default='')})
				vul_name = parent_obj.findtext('alert',default='')
				desc = parent_obj.findtext('desc',default='')
				cwe = parent_obj.findtext('cweid',default='')
				solution = parent_obj.findtext('solution',default='')
				severity = parent_obj.findtext('riskcode',default=0)
				confidence = parent_obj.findtext('confidence',default=2)
				vul_dict = init_es
				vul_dict['vulnerability'] = {
					'name':re.sub('<[^<]+?>', '',vul_name),
					'is_false_positive':False,
					'is_remediated':False,
					'tool':'ZAP',
					'confidence':confidence,
					'severity':severity,
					'description':re.sub('<[^<]+?>', '',desc),
					'vul_type':'Insecure Coding',
					'remediation':re.sub('<[^<]+?>', '',solution),
					'created_on':created_on
				}
				vul_dict['vulnerability']['evidences'] = url_param_list
				vul_dict['vulnerability']['cwe'] = {
					'cwe_id':cwe,
					'cwe_link':'https://cwe.mitre.org/data/definitions/%s.html'%cwe
				}
				write_results(vul_dict)
	except BaseException as e:
		log_exception(e)
	else:
		print('ZAP XML Parsing Completed')
