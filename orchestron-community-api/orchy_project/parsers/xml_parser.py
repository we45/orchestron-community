from django.utils import timezone
import lxml.etree as xml
from os import path
from api.utils import log_exception
from api.utils import write_results
from parsers.exceptions import MalFormedXMLException
from datetime import datetime

class Parser:
	"""
	This view is for parsing an xml file with the tool of user's choice
	"""
	def __init__(self,xml_file,user,init_es,tool):
		self.xml_file = xml_file
		self.user = user
		self.vul_dict = init_es				
		self.tool = tool

	def get_root(self):
		"""
		Raises an exeption if there is any error in the xml file
		"""
		try:
			report = xml.parse(self.xml_file)
			root_elem = report.getroot()
			return root_elem
		except (xml.XMLSyntaxError,xml.ParserError):
			raise MalFormedXMLException(self.user)
		return None

	def write_results(self,vul_name,obs,severity,desc,remedy,cves,cwes,evidences):
		"""
		Writes the results after parsing, into the ES
		"""
		self.vul_dict['vulnerability'] = {
			'name':vul_name,
			'observations':obs,
            'is_false_positive':False,
            'is_remediated':False,
            'is_deleted':False,
            'tool':self.tool,
            'severity':severity,
            'description':desc,
            'vul_type':'Insecure Configuration',
            'remediation':remedy,                
            'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            'evidences':evidences,
            'cve':cves,
            'cwe':cwes
		}
		write_results(self.vul_dict)

	def console_log(self):
		"""
		Prints a status message that the XML parsing has been completed on the console
		"""
		print('[ + ] {0} XML parsing completed'.format(self.tool))

	def get_exploits(self,cve):
		"""
		Gets all the exploits from vfeed
		"""
		try:
			vfeed = vFeed(cve)
			msf_exploits = 1 if vfeed.get_msf() else 0
			edb_exploits = 1 if vfeed.get_edb() else 0
		except Exception:
			msf_exploits = edb_exploits = 0
		return (msf_exploits,edb_exploits)

		

