from tools import tcp_port_scan
from itertools import product
from multiping import multi_ping
import paramiko
from concurrent.futures import ThreadPoolExecutor
import time
class Protocol_Exec:
    def __init__(self,protocol=None,address=None,port=None,param={}) -> None:
        self.protocol=protocol
        self.address=address
        self.port=port
        self.param=param
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
        
       
    def ftp(self):
        pass
   
    def tftp(self):
        pass
    def telnet(self):
        pass
    def ssh(self):
        print('goto send...')
        return
        ssh_client = paramiko.SSHClient()   
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
        connects=list(product(self.address,self.port,self.param['user'],self.param['pwd']))
        def send_command(connect,cmd):
            ssh_client.connect(*connect)
            command=ssh_client.invoke_shell()
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
    def exec(self):
        PROTOCOL_MAP={
            'ping':self.ping,
            'tcping':self.tcping,
            'arping':self.arping,
            'telnet':self.telnet,
            'ssh':self.ssh,
            'ftp':self.ftp,
            'tftp':self.tftp,
            'serial':self.serial
        }
        # PROTOCOL_MAP[self.protocol]()
        try:
            PROTOCOL_MAP[self.protocol]()
        except Exception as e:
            print(e)
 
if __name__ =='__main__':
    p=Protocol_Exec()
    