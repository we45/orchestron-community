import lxml.etree as xml
from api.utils import log_exception
from api.utils import write_results
from datetime import datetime


def parser_findsecbug(xml_file,user_name=None,init_es={}):
	try:
		print('FindSecBugs XML parsing initiated')
		vul_dict = {}
		data = xml.parse(xml_file)   
		data = data.getroot()
		path = data.xpath(r'//BugInstance[@category="SECURITY"]')
		all_list = []
		# Lower the priority, higher the confidence
		confidence_dict = {
			'5': 1, '3': 1,
			'2': 2, '1': 3
		}
		# Higher the rank, lower the severity.[Max rank = 20]
		severity_dict = {
			'4': 0,
			'3': 1,
			'2': 2,
			'1': 3,
			'0': 3
		}

		def evidence_return(file_path, start_line, end_line):
			d = {
				'name': 'File: {0} LineNum: {1} - {2}'.format(file_path.split('/')[-1], start_line, end_line),
				'url': file_path,
				'log': ''
			}
			return d

		for instance in path:
			evidence_list = []
			name = instance.findtext('ShortMessage')
			cwe = instance.get('cweid',0)
			confidence = confidence_dict.get(instance.get('priority'))
			severity = severity_dict.get(str(int(round(int(instance.get('rank')))/5)))
			description = instance.findtext('LongMessage')
			remediation = ''
			for sourceline in instance.findall('SourceLine'):
				d = evidence_return(file_path=sourceline.get('sourcepath'), start_line=sourceline.get('start'), end_line=sourceline.get('end'))
				evidence_list.append(d)
			for sourceline in instance.findall('Class/SourceLine'):
				d = evidence_return(file_path=sourceline.get('sourcepath'), start_line=sourceline.get('start'), end_line=sourceline.get('end'))
				evidence_list.append(d)
			for sourceline in instance.findall('Method/SourceLine'):
				d = evidence_return(file_path=sourceline.get('sourcepath'), start_line=sourceline.get('start'), end_line=sourceline.get('end'))
				evidence_list.append(d)
			if name in vul_dict:
				vul_dict[name]['evidence_list'] + evidence_list
			else:
				vul_dict[name] = {'cwe': cwe, 'description': description, 'evidence_list': evidence_list, 'confidence': 2, 'severity': 2, 'remediation': remediation}
			vul_dict[name]['confidence'] = confidence
			vul_dict[name]['severity'] = severity
		des_path = data.xpath(r'//BugPattern[@category="SECURITY"]')
		for instance in des_path:
			name = instance.findtext('ShortDescription')
			if name in vul_dict:
				vul_dict[name]['remediation'] = instance.findtext('Details')
			else:
				print('Vul not found')

		result_dict = init_es
		for vul in vul_dict.keys():
			result_dict['vulnerability'] = {
				'name': vul,
				'is_false_positive': False,
				'is_remediated': False,
				'is_deleted': False,
				'tool': 'FindSecBugs',
				'confidence': vul_dict.get(vul).get('confidence'),
				'severity': vul_dict.get(vul).get('severity'),
				'description': vul_dict.get(vul).get('description', ''),
				'remediation': vul_dict.get(vul).get('remediation', ''),
				'created_on':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				'cwe': {
					'cwe_id': vul_dict.get(vul).get('cwe', 0),
					'cwe_link': 'https://cwe.mitre.org/top25/index.html#CWE-{0}'.format(vul_dict.get(vul).get('cwe', 0))
				},
				'evidences': vul_dict.get(vul).get('evidence_list', [])

			}
			write_results(result_dict)
	except BaseException as e:
		log_exception(e)
	else:
		print('FindSecBugs XML parsing complete')
