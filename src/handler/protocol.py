from tools import tcp_port_scan,ping_scan
from itertools import product
import paramiko
from concurrent.futures import ThreadPoolExecutor
import time
from global_var import Global_Var

class Param_Error(ValueError):
    def __init__(self,error) -> None:
        super().__init__(self)
        self.error=error
    def __str__(self) -> str:
        return self.error

'''
    Param_Product:
        get_ssh_shell_P
        excute_ssh_cmd_P
        ping_P
        tcping_P
    
    此类主要负责Protocol_Excute类函数参数的构造和参数异常时的异常抛出
'''
class Param_Produce:
    
    def __init__(self,param) -> None:
        self.param=param
    def get_ssh_shell_P(self):
        '''
        return : [(address:str,port:int,username:str,password:str),...]
        '''
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

    def excute_ssh_cmd_P(self):
        pass
    def ping_P(self):
        '''
        return : {'address':[address:str],'timeout':float,'retry':int }
        '''
        if len(self.param['address'])>65535:
            raise Param_Error(
        'cannot send icmp echo request to more \
than 65535 addresses at the same time.')
        
        if 'param' not in self.param:
            timeout=1.0
            retry=5
            flag='openclose'
        else:
            if 'timeout' not in self.param['param']:
                timeout=1.0
            else:
                timeout=self.param['param']['timeout']

            if 'retry' not in self.param['param']:
                retry=5
            else:
                retry=self.param['param']['retry']

            if 'flag' not in self.param['param']:
                flag='openclose'
            else:
                flag=self.param['param']['flag']
        return {
                'address':self.param['address'],
                'timeout':timeout,
                'retry':retry,
                'flag':flag
                }
    
    def tcping_P(self):
        '''
        return : {'connect':[('address':str,'port':int),...],'timeout':int,flag:'str'}
        '''
        if 'port' not in self.param:
          raise Param_Error('the port parameter cannot be missing')
        if 'param' not in self.param:
            timeout=1
            flag='openclose'
        else:
            if 'timeout' in self.param['param']:
                timeout=self.param['param']['timeout']
            else:
                timeout=1
            if 'flag' not in self.param['param']:
                flag='openclose'
            else:
                flag=self.param['param']['flag']

        port=[i for i in self.param['port']]
        address=self.param['address']
        return {
                'connect':list(product(address,port)),
                'timeout':timeout,
                'flag':flag
                }
'''
    Protocol_Excute:
        ping:探测存活IP
        tcping:探测开放端口
        get_ssh_shell:建立一个ssh隧道
        excute_ssh_cmd:向ssh隧道发送命令
    
    此类主要负责命令执行和命令行上下文管理
'''
class Protocol_Excute:
    _exist=False
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance   
   
    def __init__(self):  
        if self._exist==False:
            self._exist=True
            self.ssh_shells=[]
            self.var=Global_Var()
            self.tcping_P=None
            self.ping_P=None
            self.excute_ssh_cmd_P=None
            self.get_ssh_shell_P=None

    def state_change(self,next_state):
        self.var.next_state=next_state

    def tcping(self,param):
        #获取参数
        self.tcping_P=Param_Produce(param).tcping_P() 
        connect=self.tcping_P['connect']
        timeout=self.tcping_P['timeout']
        flag=self.tcping_P['flag']
        #执行
        result=tcp_port_scan(connect,timeout)
        if 'open' in flag:
            print(result['open'] or 'there are no open ports')
        if 'close' in flag:
            print(result['close'] or 'there are no close ports')
  
    def ping(self,param):
        #获取参数
        self.ping_P=Param_Produce(param).ping_P() 
        address=self.ping_P['address']
        timeout=self.ping_P['timeout']
        retry=self.ping_P['retry']
        flag=self.ping_P['flag']
        
        #执行
        result=ping_scan(address,timeout,retry)
        if 'open' in flag:
            print(result['open'] or 'there are no open ip')
        if 'close' in flag:
            print(result['close'] or 'there are no close ip')

    def get_ssh_shell(self,param):
        #获取参数
        self.get_ssh_shell_P=Param_Produce(param).get_ssh_shell_P() 
        #执行
        ssh_client = paramiko.SSHClient()   
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
        def connect_shell(connect):
            ssh_client.connect(*connect)
            shell=ssh_client.invoke_shell()
            return shell 
        
        with ThreadPoolExecutor(max_workers=len(self.get_ssh_shell_P)) as executor:
            futures = [executor.submit(connect_shell,connect) for connect in self.get_ssh_shell_P]
            for future in futures:
                result=future.result()
                self.ssh_shells.append(result)
        
        self.state_change('send')

    def excute_ssh_cmd(self,param):
        #获取参数
        self.excute_ssh_cmd_P=Param_Produce(param).excute_ssh_cmd_P() 
        #执行
        def send_command(shell,cmd):
            shell.send(cmd)
            time.sleep(1)
            output=shell.recv(65535).decode()
            return output
        with ThreadPoolExecutor(max_workers=len(self.ssh_shells)) as executor:
            futures = [executor.submit(send_command,shell,self.excute_ssh_cmd_P) for shell in self.ssh_shells]
            for future in futures:
                print(future.result())

    def scp(self):
        pass
    def arping(self):
        pass
    def serial(self):
        pass
    
 
if __name__ =='__main__':
    pass
    