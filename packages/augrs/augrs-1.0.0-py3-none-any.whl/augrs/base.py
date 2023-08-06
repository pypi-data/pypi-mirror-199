import os
cwd = os.getcwd()
LOCAL_PATH = cwd + '/rc/'
RESOURCE_PATH = '/shared-vol/'
NMAP_REPORT_PATH =  cwd + '/nmap_report/'
REPORT_PATH = cwd + '/exploit_report/'

# setting dict for global setting
settings = {'TTL(s)':'30','LHOSTS':'172.17.0.2'}
# open port for exploit searching 
open_port = []
exploit_and_port = {}
exploit_list = []