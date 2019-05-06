from api.utils import log_exception
from api.utils import write_results
from django.utils import timezone
import json
import inspect
import codecs

def parse_retirejs(json_file,user_name,init_es):
    try:
        print('RetireJS parsing initiated')
        with codecs.open(json_file,'r',encoding='utf-8') as fp:
            data = json.load(fp)
            sev_dict = {
                "high":3,
                "medium":2,
                "low":1
            }
            vul_dict = dict()
            for r in data:
                results = r.get('results',[])
                if results:
                    data_dict = results[0]
                    module = data_dict.get('component','')
                    version = data_dict.get('version','')
                    dep_dict = {
                        'file_paths':[]
                    }
                    related_deps = data_dict.get('parent',{})
                    if related_deps:
                        dep = related_deps.get('component','')
                        dep_dict['file_paths'].append(dep)
                    evid_dict = {
                        'url':"Module Name "+module,
                        'name':"Version "+version,
                    }
                    vuls = data_dict.get('vulnerabilities')
                    for v in vuls:
                        name = v.get('identifiers',{}).get('summary','Unknown')
                        if name not in vul_dict:
                            vul_dict[name] = {
                                'evidences':[]
                            }
                        sev = v.get('severity')
                        severity = sev_dict.get(sev,0)
                        description = v.get('identifiers',{}).get('summary','')
                        vul_dict[name].update({
                            'name': name,
                            'is_false_positive':False,
                            'is_remediated':False,
                            'tool':'RetireJS',
                            'confidence':2,
                            'severity':severity,
                            'description':description,
                            'remediation':'',
                            'created_on':timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                        })
                        vul_dict[name]['evidences'].append(evid_dict)
            for vul in vul_dict.values():
                vul_dict_final = init_es
                vul_dict_final['vulnerability'] = vul
                write_results(vul_dict_final)
    except BaseException as e:
        log_exception(e,module_name=inspect.stack()[0][3])
    else:
        print('RetireJS parsing completed')