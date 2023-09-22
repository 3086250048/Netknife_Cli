from tools import (
    tcp_port_scan,
    ping_scan,
    connect_ssh_shell,
    send_ssh_command,
    sprint

)
from handler.param import(
    Ping_Param_Product,
    Ssh_Param_Product,
    Tcping_Param_Product
)
from concurrent.futures import ThreadPoolExecutor
# from handler.var import Global_Var

import netmiko


class Protocol_Operate:
    """
        Protocol Operate 用于构建一个和协议相关的操作，比如参数的准备、
        执行,输出控制,结果返回。

        :param var:全局变量对象,单例对象。
        :param param:从ply模块传入的变量。
        :param output:输出到cli界面上的字符。
        :param result:协议操作后返回的结果。
    """
    def __init__(self,param):
        self.param=param
        self.output=''
        self.result=None
    
    
    def ready(self):
        """准备执行前的操作"""
    
    def excute(self):
        """执行"""
    
    def print_result(self):
        """打印执行结果"""

    def get_result(self,param):
        """获取输出结果"""
    
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
    