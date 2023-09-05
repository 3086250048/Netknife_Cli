from tools import tcp_port_scan
from itertools import product

class Protocol_Exec:
    def __init__(self,protocol=None,address=None,port=None,param=None) -> None:
        self.protocol=protocol
        self.address=address
        self.port=port
        self.param=param
    def tcping(self):
        if not self.port :
            print('the port parameter cannot be missing')
            return
        port=[int(i) for i in self.port]
        param={}
        param['flag']=self.param['flag'] or 'open'
        param['timeout']=self.param['timeout'] or 1
        tcp_port_scan(list(product(self.address,port)),int(param['timeout']),param['flag']) 

    def ping(self):
        pass
    def ftp(self):
        pass
    def tftp(self):
        pass
    def telnet(self):
        pass
    def ssh(self):
        pass
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
        PROTOCOL_MAP[self.protocol]()
 
if __name__ =='__main__':
    p=Protocol_Exec()
    