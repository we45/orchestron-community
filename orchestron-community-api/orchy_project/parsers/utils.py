import os
from django.conf import settings
import lxml.etree as xml
import uuid
import json
from parsers.exceptions import MalFormedXMLException
from api.utils import log_exception, validate_allowed_files
from django.utils import timezone
from dateutil import parser

def remove_file(file_name):
    """
    Removes a file of file_name which exists in the OS path
    """
    if os.path.exists(file_name):
        os.unlink(file_name)


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
    allowed = validate_allowed_files(complete_path)
    if allowed:
        return complete_path

def get_created_on(scan_date):
    current_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S") 
    try:
        if scan_date:
            created_on = parser.parse(scan_date).strftime("%Y-%m-%d %H:%M:%S") 
        else:
            created_on = current_date  
    except:
        created_on = current_date
    return created_on