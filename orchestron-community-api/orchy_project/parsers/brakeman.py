from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from random import randint 
import json
from collections import defaultdict
import inspect
import codecs


confidence_dict = {
	"High":3,
	"Medium":2,
	"Low":1
}

def parse_brakeman(json_file,user_name,init_es):
	"""
	parses the json file obtained by breakman scanner and pushes the result 
	to results to DB
	"""
	try:
		print('Brakeman json parsing initiated')
		with codecs.open(json_file, 'r',encoding='utf-8') as data_file:
			data = json.load(data_file)
			current_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S") 
			scan_date = data.get('scan_info',{}).get('end_time',current_date)
			vuls = data.get('warnings',[])			
			new_vuls = defaultdict(list)
			for v in vuls:
				param_evd = v.get('user_input','')
				filename = v.get('file','')
				line_num = v.get('line','')
				code = v.get('code','')
				evid_desc = "File :{0}, Line :{1}".format(filename,line_num)			
				new_vuls[v.get('warning_type','Unknown')].append(
					{
						'line_number'  : line_num,
						'line_range'   : '',
						'path'         : filename.split('/')[-1:][0],
						'code_snippet' : code,
						'param'        : param_evd,
						'file'         : filename
					}
				)
			for vul_name,url_param_list in new_vuls.items():
				vul_dict = init_es	
				vul_dict['vulnerability'] = {
					'name':vul_name,
					'is_false_positive':False,
					'is_remediated':False,
					'is_deleted':False,
					'tool':'Brakeman',
					'confidence':2,
					'severity':1,
					'description':'',
					'remediation':'',                
					'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
					'evidences':url_param_list
				}
				write_results(vul_dict)
	except BaseException as e:
		log_exception(e,module_name=inspect.stack()[0][3])         
	else:         
		print('JSON Parsing Completed')
