from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 
import json
from collections import defaultdict
from lxml import html


def parse_appscan_sast(full_path,user_name,init_es):
	with open(full_path) as fp:
		tree = html.fromstring(fp.read())
		names = tree.findall('body/table[@class="report_tree_link"]/tbody/tr/td/a[@class="form_link"]')
		for i,n in enumerate(names,1):
			name = str(n.text or 'Unknown').split('-')[-1]
			desc = tree.findtext('body/div[@id="div_{0}"]/table/tbody/tr/td/pre'.format(i),default='')
			bullets = tree.findall('body/div[@id="div_{0}"]/table/tbody/tr/td[@class="f8-0"]'.format(i))
			codes = tree.findall('body/div[@id="div_{0}"]/table/tbody/tr/td/div/table/tbody/td/div/table/tbody/'.format(i))
			evidences = []
			cwe = 0
			code_snippet = ''
			for c in codes:
				file_name = ''
				line_num = ''
				code_block = c.find('td[@colspan="8"]')
				if code_block is not None:
					snippet = code_block.find('div/table/tbody/tr/td[@class="code"]')
					if snippet is not None:
						snippet_child_tags = snippet.findall('.//')
						for s in snippet_child_tags:
							# print s.text_content()
							code_snippet += '{0}'.format(s.text_content())
				td4 = c.find('td[4]')
				if td4 is not None:
					file_name =  td4.text or ''
				td5 = c.find('td[5]')
				if td5 is not None:
					line_num = td5.text or ''
				td6 = c.find('td[6]/a')
				if td6 is not None:
					cwe = td6.text or 0
				if file_name and line_num:
					evid_desc = "Line : {0}".format(line_num)
					evidences.append({
						'url':file_name,
						'name':evid_desc,
						'log':code_snippet
					})
					# print code_snippet
					code_snippet = ''
			for b in bullets:
				desc += '\n{0}'.format(b.text or '')
			vul_dict = init_es	
			vul_dict['vulnerability'] = {
				'name':name,
				'is_false_positive':False,
				'is_remediated':False,
				'is_deleted':False,
				'tool':'AppScan - SAST',
				'confidence':2,
				'severity':2,
				'description':desc,
				'remediation':'',                
				'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
				'evidences':evidences
			}
			write_results(vul_dict)
		
