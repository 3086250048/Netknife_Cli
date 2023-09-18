from tools import (
    tcp_port_scan,
    ping_scan,
    connect_ssh_shell,
    send_ssh_command,
    sprint

)
from handler.param import(
    PING_Param_Product,
    SSH_Param_Product,
    TCPING_Param_Product
)
from concurrent.futures import ThreadPoolExecutor
from global_var import Global_Var

var=Global_Var()


class Protocol_Excute:
    '''
    Protocol_Excute:
        ping:探测存活IP
        tcping:探测开放端口
        get_ssh_shell:建立一个ssh隧道
        excute_ssh_cmd:向ssh隧道发送命令
    
    此类主要负责命令执行和命令行上下文管理
    '''
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
            self.tcping_param=None
            self.ping_param=None
            self.excute_ssh_cmd_param=None
            self.get_ssh_shell_param=None

    def state_change(self,next_state):
        self.var.next_state=next_state

    def ping(self,param):
        #重置ping的历史记录
        var.ping_open=None
        var.ping_close=None  
        
        #获取参数
        self.ping_param=PING_Param_Product(param).result() 
        for p in self.ping_param:
            address=p['address']
            timeout=p['timeout']
            retry=p['retry']
            flag=p['flag']
            sort=p['sort']
        
            #执行
            result=ping_scan(address,timeout,retry,sort)
            if 'open' in flag:
                print(result['open'] or 'there are no open ip')
            if 'close' in flag:
                print(result['close'] or 'there are no close ip')

    def tcping(self,param):
        #重置tcping的历史记录
        var.tcping_open=None
        var.tcping_close=None
        #获取参数
        self.tcping_param=TCPING_Param_Product(param).result() 
        for tcping_p in self.tcping_param:
            connect=tcping_p['connect']
            timeout=tcping_p['timeout']
            flag=tcping_p['flag']
            #执行
            result=tcp_port_scan(connect,timeout)
            if 'open' in flag:
                print(result['open'] or 'there are no open ports')
            if 'close' in flag:
                print(result['close'] or 'there are no close ports')
    
    def get_ssh_shell(self,param):
        #获取参数
        self.get_ssh_shell_P=SSH_Param_Product(param).get_ssh_shell_P() 
        #执行
        #清空ssh历史记录(添加记录在tools里)
        self.var.ssh_open=None
        self.var.ssh_close=None
        with ThreadPoolExecutor(max_workers=len(self.get_ssh_shell_P)) as executor:
            futures = [executor.submit(connect_ssh_shell,connect) for connect in self.get_ssh_shell_P]   
            for future in futures:
                result=future.result()
                self.ssh_shells.append(result)
        #状态切换
        self.state_change('send')

    def excute_ssh_cmd(self,param):
        #获取参数
        self.excute_ssh_cmd_P=SSH_Param_Product(param).excute_ssh_cmd_P()+'\n' 
        #执行
        with ThreadPoolExecutor(max_workers=len(self.ssh_shells)) as executor:
            futures = [executor.submit(send_ssh_command,shell,self.excute_ssh_cmd_P) for shell in self.ssh_shells]
            for future in futures:
                try:
                    print(future.result())
                except Exception as e:
                    print(e)

    def scp(self):
        pass
    def arping(self):
        pass
    def serial(self):
        pass
    
 
if __name__ =='__main__':
    pass
    