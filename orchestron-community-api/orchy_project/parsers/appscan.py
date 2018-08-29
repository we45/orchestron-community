from django.utils import timezone
from lxml import etree
import json
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime
from random import randint 
import sys
from base64 import b64encode
import os

def parse_appscan_dast(xml_file,user_name,init_es):
	"""
	parses the xml file obtained by app scan and pushes the result 
	to results to DB
	"""
	report = etree.parse(xml_file)
	root_elem = report.getroot()
	fix_recommendations = root_elem.find('fix-recommendation-group')
	url_group = root_elem.find('url-group')
	issue_group = root_elem.find('issue-group')	
	items = root_elem.findall('issue-type-group/item')
	for item in items:
		severity = item.attrib.get('maxIssueSeverity')
		ref_id = item.attrib.get('id')
		name = item.findtext('name',default='Unknown')
		cwe = item.findtext('cwe',default='0')
		recommendation_text = ''
		general = root_elem.find("fix-recommendation-group/item[@id='{0}']/general/fixRecommendation[@type='General']".format(ref_id))
		if general is not None:
			recommendation_text += '\n'.join([g.text or '' for g in general.findall('./') if g is not None])
		# dotnet = root_elem.find("fix-recommendation-group/item[@id='{0}']/asp-dot-net/fixRecommendation[@type='ASP.NET']".format(ref_id))
		# if dotnet is not None:
		# 	recommendation_text += '\n'.join([g.text or '' for g in dotnet.findall('./') if g is not None])
		# j2ee = root_elem.find("fix-recommendation-group/item[@id='{0}']/j2ee/fixRecommendation[@type='J2EE']".format(ref_id))
		# if j2ee is not None:
		# 	recommendation_text += '\n'.join([g.text or '' for g in j2ee.findall('./') if g is not None])
		# php = root_elem.find("fix-recommendation-group/item[@id='{0}']/php/fixRecommendation[@type='PHP']".format(ref_id))
		# if php is not None:
		# 	recommendation_text += '\n'.join([g.text or '' for g in php.findall('./') if g is not None])
		req_resp = issue_group.xpath("item/issue-type/ref[text()='{0}']".format(ref_id))
		evidences = []
		for r in req_resp:
			url_ref = r.getparent().getparent().findtext('url/ref',default='')
			url = root_elem.findtext('url-group/item[@id="{0}"]/name'.format(url_ref),default='')
			parameters = r.getparent().getparent().findall('variant-group/item/differences/item')
			for p in parameters:
				param_name = p.attrib.get('name','')
				new_req_resp = r.getparent().getparent().findtext('variant-group/item/test-http-traffic',default='')
				rs = new_req_resp.replace('TRACE','\n\n$$Orc$$TRACE').replace('PATCH','\n\n$$Orc$$PATCH').replace('POST','\n\n$$Orc$$POST').replace('BOGUS','\n\n$$Orc$$BOGUS').replace('GET','\n\n$$Orc$$GET').replace('PUT','\n\n$$Orc$$PUT').replace('HEAD','\n\n$$Orc$$HEAD').replace('OPTIONS','\n\n$$Orc$$OPTIONS').replace('DELETE','\n\n$$Orc$$DELETE')
				req_resp_split = rs.split('\n\n$$Orc$$')
				req = res = ''
				for a in req_resp_split:
					d = a.replace('\n\nHTTP/','##Orc##HTTP/').split('##Orc##')
					if len(d) == 2:
						if 'HTTP/' in d[0] and 'HTTP/' in d[1]:
							req = d[0]
							res = d[1]
							evid_dict = {
								'url':url,
								'name':param_name,
								'request':b64encode(bytes(req.encode('utf-8'))),
								'response':b64encode(bytes(res.encode('utf-8'))),
							}
							evidences.append(evid_dict)
		vul_dict = init_es
		vul_dict['vulnerability'] = {
			'name':name,
			'is_false_positive':False,
			'is_remediated':False,
			'is_deleted':False,
			'tool':'AppScan - DAST',
			'confidence':2,
			'severity':severity,
			'description':'N/A',
			'vul_type':'Insecure Coding',
			'remediation':recommendation_text,
			'observations':'N/A',
			'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
		}
		vul_dict['vulnerability']['evidences'] = evidences
		vul_dict['vulnerability']['cwe'] = {
			'cwe_id':cwe
		}            
		write_results(vul_dict)
