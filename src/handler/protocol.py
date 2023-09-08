from tools import tcp_port_scan
from itertools import product
from multiping import multi_ping
import paramiko
from concurrent.futures import ThreadPoolExecutor
import time
from main import Netknife
import lexyacc.send as send
class Param_Produce:
    def __init__(self,param) -> None:
        self.param=param
    def produce_ssh_param(self):
        param,user,pwd={},'',''
        param['address']=self.param['address']
        if 'port' not in self.param:
            param['port']=22
        else:
            param['port']=self.param['port']
        if 'param' not in self.param:
            while not user or not pwd :
                if not user: user=input('username:')
                if not pwd: pwd=input('password:')
                param['username']=user
                param['password']=pwd
        else:
                param['username']=self.param['param']['user']
                param['password']=self.param['param']['pwd']

        return list(product(param['address'],[param['port']],[param['username']],[param['password']]))

class Protocol_Exec:

    def __init__(self,param):    
        product_param_map={
            'ssh':Param_Produce(param).produce_ssh_param
        }
        self.ssh_connects_info=product_param_map[param['protocol']]()
        print(self.ssh_connects_info)
    def tcping(self):
        if not self.port :
            print('the port parameter cannot be missing')
            return
        port=[int(i) for i in self.port]
        param={
            'timeout':1,
        }
        if 'timeout' in self.param.keys():
            param['timeout']=int(self.param['timeout'])
        result=tcp_port_scan(list(product(self.address,port)),param['timeout'])
        if 'flag' not in self.param.keys(): 
            print(result['open'] or 'there are no open ports')
            print(result['close'] or 'there are no close ports')
        else:
            if 'open' in self.param['flag']:
                print(result['open'] or 'there are no open ports')
            if 'close' in self.param['flag']:
                print(result['close'] or 'there are no close ports')
  
    def ping(self):
        result={
            'open':'',
            'close':''
        }
        if not self.address :
            print('the address parameter cannot be missing')
            return
        else:
            if len(self.address)>65535:
                print('cannot send icmp echo request to more than 65535 addresses at the same time.')
                return
        if 'timeout' not in self.param.keys():
            timeout=1.0
        else:
            timeout=float(self.param['timeout'])

        if 'retry' not in self.param.keys():
            retry=5
        else:
            retry=int(self.param['retry'])

        mp=multi_ping(self.address,timeout,retry)
     
        result['open']=''
        result['close']=''
        for i in list(mp[0].keys()):
            result['open']+=f'ip:{i}:open\n'
        for i in mp[1]:
            result['close']+=f'ip:{i}:close\n'
      
        if 'flag' not in self.param.keys(): 
            print(result['open'].rstrip() or 'there are no open ip')
            print(result['close'] or 'there are no close ip')
        else:
            if 'open' in self.param['flag']:
                print(result['open'] or 'there are no open ip')
            if 'close' in self.param['flag']:
                print(result['close'] or 'there are no close ip')

        pass
    

    def get_ssh_shell(self):
        Netknife().change_state(send,'>')
        self.ssh_shells=[]
        ssh_client = paramiko.SSHClient()   
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
        def connect_shell(connect):
            ssh_client.connect(*connect)
            shell=ssh_client.invoke_shell()
            return shell 
        
        with ThreadPoolExecutor(max_workers=len(self.ssh_connects_info)) as executor:
            futures = [executor.submit(connect_shell,connect) for connect in self.ssh_connects_info]
            for future in futures:
                result=future.result()
                self.ssh_shells.append(result)
       
        print('ok')        

    def excute_ssh_cmd(self):
        return
        def send_command(connect,cmd):
            command.send(cmd)
            time.sleep(1)
            output=command.recv(65535).decode()
            return output
        with ThreadPoolExecutor(max_workers=len(connects)) as executor:
            futures = [executor.submit(send_command,connect,1) for connect in connects]
            for future in futures:
                print(future.result())

    def scp(self):
        pass
    def arping(self):
        pass
    def serial(self):
        pass

 
if __name__ =='__main__':
    p=Protocol_Exec()
    