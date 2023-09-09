


import paramiko
import netmiko
from concurrent.futures import ThreadPoolExecutor
import time

def get_ssh_shell():
        l=[]
        #获取参数
        get_ssh_shell_P=[('192.168.60.2',22,'root',' ')]
        #执行
        
        def connect_shell(connect):
            ssh_client = paramiko.SSHClient()   
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
            ssh_client.connect(*connect)
            shell=ssh_client.invoke_shell()
            return shell
        
        with ThreadPoolExecutor(max_workers=len(get_ssh_shell_P)) as executor:
            futures = [executor.submit(connect_shell,connect) for connect in get_ssh_shell_P]
            for future in futures:
                result=future.result()
                l.append(result)
        return l
def excute_ssh_cmd(connects,cmd):
        #获取参数
        excute_ssh_cmd_P=cmd
        #执行
        def send_command(shell,cmd):
            shell.send(cmd)
            time.sleep(1)
            output=shell.recv(65535).decode('utf-8')
            return output
        with ThreadPoolExecutor(max_workers=len(connects)) as executor:
            futures = [executor.submit(send_command,shell,excute_ssh_cmd_P) for shell in connects]
            for future in futures:
                print(future.result())


if __name__ =='__main__':
    print("""


""")