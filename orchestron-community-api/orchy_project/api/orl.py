import requests_cache
import requests
import os
from api.models import ORLConfig

requests_cache.install_cache('demo_cache')


def get_open_vul_name_from_api(cwe,org):
    BASE_URL = ORLConfig.objects.get(org=org).get_config_url()
    open_vuls_name = requests.get('{0}/name_only/{1}'.format(BASE_URL,int(cwe)))
    if open_vuls_name.json().get('commonName'):
        open_vul_name = open_vuls_name.json().get('commonName')
    else:
        open_vul_name = open_vuls_name.json().get('name')
    return open_vul_name


def get_open_vul_info_from_api(cwe,org):
    BASE_URL = ORLConfig.objects.get(org=org).get_config_url()
    open_vul_info = requests.get('{0}/get/{1}'.format(BASE_URL,int(cwe)))   
    return open_vul_info.json()


def get_cwe_from_name(name,org):
    BASE_URL = ORLConfig.objects.get(org=org).get_config_url()
    data = {
        'name':name
    }
    open_vul_info = requests.post('{0}/alias/'.format(BASE_URL),json=data)   
    return open_vul_info.json().get('cwe',0)     