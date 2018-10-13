import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[ + ] %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)