from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfrpc import JobManager

import signal
import json
import time
import os
import sys

import pyfiglet

import augrs.nmap_module as nmap_module
import augrs.exploit_module as exploit_module
import augrs.rc_module as rc_module
import augrs.base as base
import augrs.validate as validate

excellentExplotis = []
# excellentExplotis = ['unix/ftp/vsftpd_234_backdoor','windows/fileformat/activepdf_webgrabber', 'windows/fileformat/djvu_imageurl', 'windows/fileformat/mcafee_hercules_deletesnapshot', 'windows/fileformat/msworks_wkspictureinterface', 'windows/fileformat/sascam_get', 'windows/smb/ms04_007_killbill', 'windows/ftp/sami_ftpd_list']
greatExploits = []
goodExploits = []
normalExploits = []
averageExploits = []
lowExploits = []
manualExplots = []

# setting dict for global setting
settings = {'TTL(s)':30}

def main():
    
    text = "HOME"
    augrs = "AugRS"
    # Use the `figlet_format` function to generate the banner
    banner = pyfiglet.figlet_format(text)
    # Get the list of running jobs
    
    # initialize require options
    print(pyfiglet.figlet_format(augrs,font = "slant"))
    print('Starting Program...')
    password = input('Please Input MSFRPC Password\n')
    client = MsfRpcClient(password,port=55553)
    print('Please Specify Initial Input')
    ipaddr = input('Target Ip address: ')
    while validate.validate_ip_address(ipaddr) == False:
        print('Invalid Ip Address')
        ipaddr = input('Please Input New Target Ip address: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    base.settings['target_ip'] = ipaddr

    # settings['target_ip'] = input('Target Ip address: ')
    print(banner)
    while True:
        try:
            # print(banner)
            print('press [1] to go to Nmap module')
            print('press [2] to go to Exploit module')
            # print('press [3] to go to Resource Script module')
            print('press [3] to go to Options')
            print('press [99] for help')
            print('press [0] to exit')
            command = input('Input Command Here: ')

            if(command == '1'):
                # print('go to Nmap')
                os.system('cls' if os.name == 'nt' else 'clear')
                nmap_module.nmap_scan()
                print(banner)
            elif(command == '2'):
                # print('go to Exploit')
                os.system('cls' if os.name == 'nt' else 'clear')
                exploit_module.exploit(client)
                print(banner)
            # elif(command == '3'):
            #     # print('Resource ')
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     rc_module.main(client)
            elif(command == '3'):
                os.system('cls' if os.name == 'nt' else 'clear')
                __options()
                print(banner)
            elif(command == '99'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print("Basic Flow 1\t\tNmap Module --> Exploit Module --> search exploit --> run exploit")
                print("Basic Flow 2\t\tNmap Module --> Exploit Module --> generate resource script ")
                print("Nmap Module\t\tRun Nmap on your local to scan for an open port and generate a report after successfully run (Report will generate in Folder nmap_report)")
                print()
            elif(command == '0'):
                print('exiting ..')
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print('Error: Command Not Found')
        except KeyboardInterrupt:
            break
        


def __options():
    # text = "OPTIONS"
    print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
    while True:
        try:
            for key in base.settings:
                print(key + ": " + str(base.settings[key]))
            print('')
            print('press [1] to edit options')
            print('press [99] for helps')
            print('press [0] to exit')
            command = input('Input Command Here: ')

            if(command == '1'):
                os.system('cls' if os.name == 'nt' else 'clear')
                __edit_options()
                print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
                # print('current Ip address is '+settings['target_ip']) 
            elif(command == '99'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
                print('select number in front of an options to edit')
                print()
            elif(command == '0'):
                print('exiting ..')
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
                print('Error: Command Not Found')
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        # for key in base.settings:
        #     print(key + ": " + str(base.settings[key]))
        # print('')
        # print('press [1] to edit options')
        # print('press [0] to exit')
        # command = input('Input Command Here: ')

        # if(command == '1'):
        #     os.system('cls' if os.name == 'nt' else 'clear')
        #     __edit_options()
        #     print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
        #     # print('current Ip address is '+settings['target_ip']) 
        # elif(command == '0'):
        #     print('exiting ..')
        #     os.system('cls' if os.name == 'nt' else 'clear')
        #     break
        # else:
        #     os.system('cls' if os.name == 'nt' else 'clear')
        #     print(pyfiglet.figlet_format(text = "OPTIONS",font = "slant"))
        #     print('Error: Command Not Found')


def __edit_options():
    print(pyfiglet.figlet_format(text = "EDIT OPTIONS",font = "slant"))
    while True:
        try:
            settings = base.settings
            count = 0
            numkey = {}
            for key in settings:
                count+= 1
                print('['+ str(count) +'] ' + key + ": " + str(settings[key]))
                numkey[count] = key
            print('select option to edit')
            command = int(input('selected option: '))
            if(command in numkey.keys()):
                print('Current ' + str(numkey[command]) + ' is ' + str(settings[numkey[command]]))
                newvalue = input('Enter New Value: ')
                if(validate.setting_validate(numkey[command],newvalue)):
                    base.settings[numkey[command]] = newvalue
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(pyfiglet.figlet_format(text = "EDIT OPTIONS",font = "slant"))
                    print('Error: Invalid Input')
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(pyfiglet.figlet_format(text = "EDIT OPTIONS",font = "slant"))
                print('Error: Invalid Input')
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            break







if __name__ == '__main__':
    main()
