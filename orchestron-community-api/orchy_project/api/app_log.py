import logging
import logging.handlers

def app_debug_logger(msg):
    logging.getLogger('debug_logger').debug(msg)

def app_info_logger(msg):
    logging.getLogger('info_logger').info(msg)

def app_error_logger(msg):
    logging.getLogger('error_logger').error(msg)

def app_warning_logger(msg):
    logging.getLogger('warning_logger').warning(msg)

def app_critical_logger(msg):
    logging.getLogger('critical_logger').critical(msg)	

def error_logger(request,event):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to debug_logger
    output type: log data 
    template used: NA
    """
    app_critical_logger("IP - {0} ; User - {1} ; Event - {2} ; Status - failure.".format(request.get_host(),request.user.username, event))
    app_debug_logger("IP - {0} ; User - {1} ; Event - {2} ; Status - failure.".format(request.get_host(),request.user.username, event))	



def debug_log(ip,user,event,status):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to debug_logger
    output type: log data 
    template used: NA
    """
    msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
    logging.getLogger('debug_logger').debug(msg)

def info_log(ip,user,event,status):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to info_logger
    output type: log data 
    template used: NA
    """
    msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
    logging.getLogger('info_logger').info(msg)

def error_log(ip,user,event,status):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to error_logger
    output type: log data 
    template used: NA
    """
    msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
    logging.getLogger('error_logger').error(msg)

def warning_log(ip,user,event,status):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to warning_logger
    output type: log data 
    template used: NA
    """
    msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
    logging.getLogger('warning_logger').warning(msg)

def critical_log(ip,user,event,status):
    """
    input description: parameters: IP (host), Username, event, status
    input type: hear the username name is unicode, rest of the parameter is string
    action preformed:logging
    output descritpion: Logs of all activities on Orchestron Console are logged to critical_logger
    output type: log data 
    template used: NA
    """
    msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
    logging.getLogger('critical_logger').critical(msg)


####################
def info_debug_log(ip=None,user=None,event=None,status=None):
	msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
	logging.getLogger('info_logger').info(msg)
	logging.getLogger('debug_logger').debug(msg)

def error_debug_log(ip=None,user=None,event=None,status=None):
	msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
	logging.getLogger('error_logger').error(msg)
	logging.getLogger('debug_logger').debug(msg)

def warning_debug_log(ip=None,user=None,event=None,status=None):
	msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
	logging.getLogger('warning_logger').warning(msg)
	logging.getLogger('debug_logger').debug(msg)

def critical_debug_log(ip=None,user=None,event=None,status=None):
	msg = "IP - {0}; User - {1} ; Event - {2} ; Status - {3}".format(ip,user,event,status)
	logging.getLogger('critical_logger').critical(msg)
	logging.getLogger('debug_logger').debug(msg)
