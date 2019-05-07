from django.utils import timezone
import lxml.etree as xml
import os
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 
import json
from collections import defaultdict
import codecs

sev_dict = {
	"LOW":1,
	"MEDIUM":2,
	"HIGH":3
}



script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'safety_db.json')


def parse_safety(json_file,user_name,init_es):
	"""
	parses the json file obtained by bandit scanner and pushes the result 
	to results to DB
	"""
	try:
		safety_db_results = json.load(open(file_path,'r'))
		safety_data = []
		print("Safety json parsing initiated")
		with codecs.open(json_file,'r',encoding='utf-8') as fp:
			datafile = json.load(fp)
			for result in datafile:
				safety_dict = {}
				res_id = "pyup.io-{0}".format(result[4])
				for k,v in safety_db_results.items():
					for k in v:
						if res_id == k.get("id",""):
							safety_dict['vulnerability_name'] = "{0} {1}".format(result[0],result[2])
							safety_dict['package_name'] = result[0]
							safety_dict['version'] = result[2]
							safety_dict['description'] = result[3]
							safety_dict['CVE'] = k.get("cve",0)
							safety_dict['remediation'] = k.get("advisory","")
							safety_data.append(safety_dict)
		for safe in safety_data:
			url_param_list = []
			url_param_list.append({
				'url':"Module "+safe.get("package_name",""),
				'name':"Version "+safe.get("version",""),
			})
			vul_dict = init_es
			vul_dict['vulnerability'] = {
				'name':safe.get("vulnerability_name",""),
				'is_false_positive':False,
				'is_remediated':False,
				'is_deleted':False,
				'tool':'Safety',
				'confidence':2,
				'severity':2,
				'description':safe.get("description",""),
				'remediation':safe.get("remediation",""),
				'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
				'evidences':url_param_list,
			}
			write_results(vul_dict)
	except Exception as e:
		print(e)
	else:
		print('JSON Parsing Completed')