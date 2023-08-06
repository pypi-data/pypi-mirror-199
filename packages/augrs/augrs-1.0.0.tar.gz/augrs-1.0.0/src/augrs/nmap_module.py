import nmap3
import json
import augrs.base as base
import datetime
import augrs.validate as validate
import os
import platform

def nmap_scan():
    nmap = nmap3.Nmap()
    date = datetime.datetime.now()
    ip_address = base.settings['target_ip']
    version_result = ''
    home_path = os.path.expanduser("~")
    # Specify the folder name
    folder_name = "AugRS_nmap_report"
    folder_path = os.path.join(home_path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        # print(f"Created folder {folder_name} in the home directory.")
    while True:
        try:
            if(validate.validate_ip_address(ip_address)): 
                # ip_address = base.settings['target_ip']
                print('Scanning for ip = '+ip_address)
                version_result = nmap.nmap_version_detection(base.settings['target_ip'],args ="-Pn") 
                json_formatted_str = json.dumps(version_result, indent=4,sort_keys=True)
                jj = json.loads(json_formatted_str)
                data = jj[ip_address]['ports']
                if platform.system() == "Windows":
                    # os.system(f"cd {folder_path} && echo 'This is a Windows file' > {file_name}")
                    # print(f"Created Windows file {file_name} inside {folder_name}.")
                    gen_report(ip_address,data,date,folder_path)
                    print('Report Create in ' + folder_path)                 
                    break
                elif platform.system() == "Linux":
                    gen_report(ip_address,data,date,folder_path)
                    print('Report Create in ' + folder_path)                
                    break
                else:
                    print("Unknown operating system.")            
                    break 
            else:
                print('Error: Invalid Ip address')
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            print('Error: Please try again')
            break
    

def gen_report(ip_address,data,date,folder_path):
    with open(folder_path + '/' + ip_address + '_'+ str(date.date()) +'.txt', 'w') as f:
        f.write("IP: %s\n" % ip_address)
        print("IP: %s" % ip_address)
        for port in data:
            # 4 case 
            # have all information
            # print(port)
            base.open_port.append(port['portid'])
            if(port['state'] == 'open' and 'version' in port['service'].keys() and 'product' in port['service'].keys()):
                print('PORT: ' +port['portid']+'/'+port['protocol'] +' SERVICE: '+port['service']['name'] + ' VERSION: ' + port['service']['product'] + ' ' + port['service']['version'])
                f.write('PORT: ' +port['portid']+'/'+port['protocol'] +' SERVICE: '+port['service']['name'] + ' VERSION: ' + port['service']['product'] + ' ' + port['service']['version'])
                f.write('\n')
            elif(port['state'] == 'open' and 'version' in port['service'].keys()): # have only version keys
                # print('Im only have version key!!')
                print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['version'])
                f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['version'])
                f.write('\n')
            elif(port['state'] == 'open' and 'product' in port['service'].keys()): # have only product keys 
                # print('Im only have product key!!')
                print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['product'])
                f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['product'])
                f.write('\n')
            elif(port['state'] == 'open'): # dont have version and product keys
                # print('Im dont have both extras keys!!')
                print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name'] + ' VERSION: ')
                f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name'] + ' VERSION: ')
                f.write('\n')
    
    

def main():
    print('nmap module')
# This line runs the main function
if __name__ == "__main__":
    main()