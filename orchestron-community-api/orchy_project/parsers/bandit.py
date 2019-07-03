from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from random import randint
import json
from collections import defaultdict
from dateutil import parser
import inspect

sev_dict = {
	"LOW":1,
	"MEDIUM":2,
	"HIGH":3
}

def parse_bandit(json_file,user_name,init_es):
	"""
	parses the json file obtained by bandit scanner and pushes the result
	to results to DB
	"""
	try:
		print("Bandit json parsing initiated")
		with open(json_file,'r',encoding='utf-8') as fp:
			datafile = json.load(fp)
			current_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
			scan_date = datafile.get('generated_at',current_date)
			created_on = parser.parse(scan_date).strftime("%Y-%m-%d %H:%M:%S")
			results = datafile.get('results',[])
			new_vuls = defaultdict(list)
			for r in results:
				filename = r.get('filename','')
				code = r.get('code','')
				line_num = r.get('line_number','')
				line_range = r.get('line_range') or ''
				if line_range:
					line_range = line_range[-1]
				evid_desc = "File :{0}, Line :{1}".format(filename,line_num)
				new_vuls[(r.get('test_name','Unknown'),r.get('issue_severity','LOW'))].append(
					{
						'line_number'  :  line_num,
						'line_range'   :  line_range,
						'path'         :  filename.split('/')[-1:][0],
						'code_snippet' :  code,
						'param'        :  'NA',
						'file'         :  filename
					}
				)
			for vul_tup,url_param_list in new_vuls.items():
				vul_dict = init_es
				vul_dict['vulnerability'] = {
					'name':vul_tup[0],
					'is_false_positive':False,
					'is_remediated':False,
					'is_deleted':False,
					'tool':'Bandit',
					'confidence':2,
					'severity':sev_dict.get(vul_tup[1],0),
					'description':'',
					'remediation':'',
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'evidences':url_param_list
				}
				write_results(vul_dict)
	except Exception as e:
		log_exception(e,module_name=inspect.stack()[0][3])
	else:
		print('Bandit JSON Parsing Completed')


