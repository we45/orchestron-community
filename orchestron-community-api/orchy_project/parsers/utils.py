import os
from django.conf import settings
import lxml.etree as xml
import uuid
import json
from parsers.exceptions import MalFormedXMLException
from api.utils import log_exception

def remove_file(file_name):
    """
    Removes a file of file_name which exists in the OS path
    """
    if os.path.exists(file_name):
        os.unlink(file_name)



def validate_allowed_files(flat_file,user):
    """
    Parse the xml and verify whether the xml header is under the valid uploadable xml files list
    """
    try:
        ext = flat_file.split('.')[-1]
        print(ext)
        if ext == 'json':
            with open(flat_file) as data_file:
                data = json.load(data_file)
                is_brakeman = data.get('scan_info',{}).get('brakeman_version')
                is_bandit = data.get('results',[])
                is_arachni = data.get('issues',[])
                if is_brakeman:
                    return 'Brakeman'
                elif is_bandit:
                    return 'Bandit'
                elif is_arachni:
                    return 'Arachni'
                else:
                    return None
        elif ext == 'xml':
            try:
                nreport = xml.parse(flat_file)  
                root_elem = nreport.getroot()
                if root_elem is not None:            
                    header = settings.HEADER_MAP.get(root_elem.tag)
                    if header:            
                        return header
                    else:
                        remove_file(flat_file) 
                return None
            except (xml.XMLSyntaxError,xml.ParserError):
                raise MalFormedXMLException(user)
                return None
        elif ext == 'html':
            try:
                nreport = xml.parse(flat_file)  
                root_elem = nreport.getroot()
                if root_elem is not None:            
                    header = settings.HEADER_MAP.get(root_elem.tag)
                    if header:            
                        return header
                    else:
                        remove_file(flat_file) 
                return None
            except (xml.XMLSyntaxError,xml.ParserError):
                raise MalFormedXMLException(user)
                return None
        else:
            return None
    except BaseException as e:
        log_exception(e)
        return None


def validate_flat_file(file_name):
    """
    Check whether the uploaded file has the extension ".xml" 
    """
    file_root, file_ext = os.path.splitext(file_name)
    if file_ext in ['.xml','.json','.html']:        
        return True
    return False

def unique_file_path(file_name):
    """
    Returns a unique file path such that there is no ambiguity in file names
    """    
    file_root, file_ext = os.path.splitext(file_name)    
    uniq_name = "%s%s" % (uuid.uuid4(), file_ext)
    return uniq_name    

def upload_to_server(file_name,temp_file_obj,user):
    """
    Create a new file in server file system for temporary storage i.e until the parser completes its action
    """   
    if not os.path.exists(settings.XML_ROOT):
        os.makedirs(settings.XML_ROOT)
    else:
        pass
    complete_path = os.path.join(settings.XML_ROOT,file_name)
    with open(complete_path,'wb') as fp:
        fp.write(temp_file_obj.read())
    allowed = validate_allowed_files(complete_path,user)
    if allowed:
        return complete_path