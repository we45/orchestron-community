import lxml.etree as xml
from api.utils import write_results
from django.utils import timezone

def parse_xanitizer(xml_file,user_name,init_es):
	try:
		data = xml.parse(xml_file)   
	except (xml.XMLSyntaxError,xml.ParserError):
		raise MalFormedXMLException(user_name)
	data = data.getroot()
	path = data.xpath(r'//XanitizerFindingsList')
	print("xanitizer parsing initiated")
	for main in path :
		for finding in main.findall('finding'):
			problemType = finding.findtext("problemType")
			rating = finding.findtext("rating")
			result_rating = int(float(rating))
			try:
				cwehead,cweNumber = finding.findtext("cweNumber").split('-')
			except:
				cweNumber=0
			description = finding.findtext("description")
			startNode = finding.findtext("startNode")
			node = finding.findall("node")
			start_node =finding.findall("startNode")
			classification = finding.findtext("classification")
			severity ={}
			if classification == 'Must Fix':
				severity['HIGH'] = 3
				severity_name =  'HIGH'
			elif classification == 'Warning':
				severity['Medium'] =2
				severity_name = 'Medium'
			elif classification == 'Information':
				severity['Low'] =1
				severity_name =  'Low'
			elif classification == 'Harmless':
				severity['Info'] =0
				severity_name =  'Info'
			for startNode in start_node:
				keys = startNode.keys()
				evids=[]
				for items, key in enumerate(keys):
					if key == "absolutePath" :
						absolutePath = startNode.values()[items]
						evids.append({"url":absolutePath})

			for dictnode  in node:
				keys = dictnode.keys()
				evids=[]
				for  items, key in enumerate(keys):
					if key == "absolutePath" :
						absolutePath = dictnode.values()[items]
						evids.append({"url":absolutePath})

			vul_dict = init_es
			vul_dict['vulnerability'] = {
				'name': problemType,
				'is_false_positive':False,
				'is_remediated':False,
				'is_deleted':False,
				'tool':'xanitizer',
				'confidence':result_rating,
				'severity':severity.get(severity_name),
				'description': description,
				'vul_type':'Insecure Coding',
				'remediation':'',
				'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
			}
			vul_dict['vulnerability']['evidences'] = evids
			vul_dict['vulnerability']['cwe'] = {
						'cwe_id':cweNumber,
						'cwe_link':'https://cwe.mitre.org/data/definitions/%s.html'%cweNumber
					}		

			write_results(vul_dict)
	print("xanitizer parsing completed")

