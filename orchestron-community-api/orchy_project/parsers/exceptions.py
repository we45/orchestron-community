
import json

class MalFormedXMLException(Exception):
	def __init__(self,user,*args,**kwargs):
		print('Invalid XML')


