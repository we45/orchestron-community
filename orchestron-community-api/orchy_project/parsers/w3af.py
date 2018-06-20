from api.utils import log_exception
from parsers.xml_parser import Parser
from base64 import b64encode

class W3afParser(Parser):
    """
    This view is for parsing the xml file using W3af tool
    """
    def parse_xml(self):
        root_elem = self.get_root()
        if root_elem is not None:                 
            try:
                vuls = root_elem.findall('vulnerability')   
                severity_dict = {
                    'Information':0,
                    'Low':1,
                    'Medium':2,
                    'High':3
                }     
                uniq_objs = root_elem.findall('vulnerability')
                vuls = set([i.attrib.get('name','Unknown') for i in uniq_objs])     
                p = 'vulnerability[@name = $name]'
                for v in vuls:
                    cves = []
                    cwes = {}
                    url_param_list = []         
                    obj = root_elem.xpath(p,name=v)   
                    for parent_obj in obj:                        
                        url = parent_obj.attrib.get('url','')
                        param = parent_obj.attrib.get('var','')
                        trans = parent_obj.find('http-transactions')   
                        if trans is not None:         
                            req_resps = trans.findall('http-transaction')
                            request = response = '\n'
                            for r in req_resps:
                                req = r.find('http-request')                
                                request += req.findtext('status',default='')
                                headers = req.findall('headers/header')
                                for h in headers:
                                    request += '\n%s:%s'%(h.attrib.get('field'),h.attrib.get('content'))
                                res = r.find('http-response')                
                                response += res.findtext('status',default='')
                                headers = res.findall('headers/header')
                                for h in headers:
                                    response += '\n%s:%s'%(h.attrib.get('field'),h.attrib.get('content'))                              
                            url_param_list.append({
                                'url':url,
                                'name':param,
                                'request':b64encode(request),
                                'response':b64encode(response)
                            })              
                    vul_name = parent_obj.attrib.get('name','Unknown')
                    desc = parent_obj.findtext('long-description',default='')
                    remedy = parent_obj.findtext('fix-guidance',default='')
                    severity = severity_dict.get(parent_obj.attrib.get('severity','Information'))
                    self.write_results(vul_name,'',severity,desc,remedy,cves,cwes,url_param_list)            
            except BaseException as e:
                log_exception(e)                
            else:        
                self.console_log()   



