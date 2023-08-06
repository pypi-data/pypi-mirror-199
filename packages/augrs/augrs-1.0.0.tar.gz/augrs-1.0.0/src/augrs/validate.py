import ipaddress
import re

def validate_ip_address(ip_string):
   try:
       ip_object = ipaddress.ip_address(ip_string)
       return True
   except ValueError:
       return False

def setting_validate(fieldname,value):
    if(fieldname == 'target_ip'):
        return validate_ip_address(value)
    elif(fieldname == 'TTL(s)'):
        return value.isdigit()
    
def is_valid_filename(filename):
    # Define a regular expression to match valid filenames
    pattern = r"^[a-zA-Z0-9_-]+$"
    
    # Use the regular expression to check whether the filename matches the pattern
    match = re.match(pattern, filename)
    
    # If there's a match, return True; otherwise, return False
    if match:
        return True
    else:
        return False