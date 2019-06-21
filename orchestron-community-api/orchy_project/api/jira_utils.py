import re
from jira import JIRA
from django.conf import settings
import hashlib
from jira.exceptions import JIRAError
import os
from uuid import uuid4
from time import sleep
from api.app_log import *
from api.ciphertext_manager import JIRACipher


def get_jira_con(jira_config):
	try:
		sleep(2)	
		cipher = JIRACipher()
		pwd = str(cipher.decrypt(jira_config.password))
		uname = str(cipher.decrypt(jira_config.username))
		url = str(jira_config.url)	
		options = {'server':url}
		jira = JIRA(options=options,basic_auth=(uname,pwd))
		if jira:
			return jira
		else:
			return None
	except BaseException as e:
		critical_debug_log(event=e,status='failure')
		return None


def test_jira_connection(url,uname,pwd):
	try:
		options = {'server':url}
		jira = JIRA(options=options,basic_auth=(uname,pwd))
		if jira:
			return True
		else:
			return False
		info_debug_log(event='Test Jira Connection',status='success')
	except BaseException as e:
		log_exception(e)
		return False


def get_projects(jira_config):
	jira_con = get_jira_con(jira_config)
	if jira_con:
		return jira_con.projects()
	else:
		return []


def get_issuetypes(jira_config):
	jira_con = get_jira_con(jira_config)
	if jira_con:
		return jira_con.issue_types()
	else:
		return []		


def get_groups(jira_config):
	jira_con = get_jira_con(jira_config)
	if jira_con:
		return jira_con.groups()
	else:
		return []		


def get_users(jira_config):
	jira_con = get_jira_con(jira_config)
	if jira_con:
		try:
			users = set()
			groups = jira_con.groups()
			for g in groups:
				try:
					members = jira_con.group_members(g)
					for member,member_dict in members.items():
						if member_dict.get('active'):
							users.add(member)
				except:
					pass
			return users
		except:
			return []
	else:
		return []		





