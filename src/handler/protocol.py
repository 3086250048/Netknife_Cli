from tools import (
    tcp_port_scan,
    ping_scan,
    connect_ssh_shell,
    send_ssh_command,
    extend_param_get
)
from itertools import product
from concurrent.futures import ThreadPoolExecutor
from global_var import Global_Var

var=Global_Var()

class Param_Error(ValueError):
    def __init__(self,error) -> None:
        super().__init__(self)
        self.error=error
    def __str__(self) -> str:
        return self.error


class Param_Produce:
    '''
    Param_Product:
        get_ssh_shell_P
        excute_ssh_cmd_P
        ping_P
        tcping_P
    
    此类主要负责Protocol_Excute类函数参数的构造和参数异常时的异常抛出
    '''
    def __init__(self,param) -> None:
        self.param=param
    def get_ssh_shell_P(self):
        '''
        return : [(address:str,port:int,username:str,password:str),...]
        '''
        param,user,pwd={},'',''
        param['address']=self.param['address']
        if 'port' not in self.param:
            param['port']=[22]
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

        return list(product(param['address'],param['port'],[param['username']],[param['password']]))

    def excute_ssh_cmd_P(self):
        return self.param
    def ping_P(self):
        '''
        return:{
            address:[address:str],
            timeout:float,
            retry:int,
            flag:str,
            sort:str
        }
        '''
     
        if 'ip' in self.param or 'ip_port' in self.param\
            or 'ip_port_user_pwd' in self.param:
            address=[ip for ip in self.param['ip']]+\
            [connect[0] for connect in self.param['ip_port']]+\
            [shell[0] for shell in self.param['ip_port_user_pwd']]
            if len(address)>65535:
                raise Param_Error(
                        'cannot send icmp echo request to more \
                than 65535 addresses at the same time.')

            '''extend_param_get函数只是给temp_ip_about_param全局变量赋值，
             所以要从temp_ip_about_param中取值
            '''
            # 重置临时ip相关参数字典
            var.temp_ip_about_param=None
            #给temp_ip_about_param赋值
            extend_param_get({
                'ip':address,
                'key':[
                    'timeout',
                    'retry',
                    'flag',
                    'sort'
                ]
            })
            ping_var=var.temp_ip_about_param
       
            #将相同ping参数的IP归类到一个列表中,并提取有参数的IP   
            
            has_param_ip=[]
            type_list=[[]]
            #对@protocol中所选中的ip按照参数进行分类
            if ping_var:   
                for key,value in ping_var.items():
                    if not type_list[0]:
                        type_list[0].append({'ip':key,'param':value})
                        has_param_ip.append(key)
                        continue
                    append=True
                    for type_p in type_list:
                        if value == type_p[0]['param']:
                            append=False
                            type_p.append({'ip':key,'param':value})
                            has_param_ip.append(key)
                    if append:
                        type_list.append([{'ip':key,'param':value}])
                        has_param_ip.append(key)
            #筛选出没有参数的ip(只针对@protocl所得到的ip),使用默认参数执行
            no_has_param_ip=[ ip for ip in address if ip not in has_param_ip]
            #没有参数的ip使用默认参数执行
            if no_has_param_ip:
                yield{
                    'address':no_has_param_ip,
                    'timeout':1.0,
                    'retry':5,
                    'flag':'openclose',
                    'sort':'forward'
                }
            #有参数的ip,则按照参数进行分组后的列表进行分别执行
            if type_list[0]:
                for type_p in type_list:
                    p=type_p[0]['param']
                    ip=[]
                    for each_dic in type_p:
                        ip.append(each_dic['ip'])
                    yield{
                        'address':ip,
                        'timeout':p.get('timeout',1.0),
                        'retry':p.get('retry',5),
                        'flag':p.get('flag','openclose'),
                        'sort':p.get('sort','forward')
                    }
                

        #判断是否是ping x.x.x.x [@ ...]句型,不是则终止
        if 'address' in self.param : 
            if len(self.param['address'])>65535:
                raise Param_Error(
            'cannot send icmp echo request to more \
than 65535 addresses at the same time.')
            else:
                if 'param' not in self.param:self.param['param']={}
                yield {
                    'address':self.param.get('address'),
                    'timeout':self.param['param'].get('timeout',1.0),
                    'retry':self.param['param'].get('retry',5),
                    'flag':self.param['param'].get('flag','openclose'),
                    'sort':self.param['param'].get('sort','forward')
                    }
                

    def tcping_P(self):
        '''
        return : {'connect':[('address':str,'port':int),...],'timeout':int,flag:'str'}
        '''
        #@协议中包含ping时的处理逻辑
        if 'ip' in self.param:
            port=[]
            wait_scan_ip=self.param['ip']
            print(f'wait_scan_ip=>{wait_scan_ip}')
            port.append(int(input('port:')))
            yield {
            'connect':list(product(wait_scan_ip,port)),
            'timeout':timeout,
            'flag':flag
            }
        #@协议中包含tcping时的处理逻辑 
        if 'ip_port' in self.param:
            yield {
                    'connect':self.param['ip_port'],
                    'timeout':timeout,
                    'flag':flag,    
                }
        #@协议中包含ssh时的处理逻辑
        if 'ip_port_user_pwd' in self.param:
            ip_port=[shell[0:2] for shell in self.param['ip_port_user_pwd']]
            yield{
                'connect':self.param['ip_port'],
                'timeout':timeout,
                'flag':flag,    
            }


        if 'port' not in self.param:
        #   raise Param_Error('the port parameter cannot be missing')
            port=[]
            wait_scan_ip=self.param['address']
            print(f'wait_scan_ip=>{wait_scan_ip}')
            port.append(int(input('port:')))
            self.param['port']=port
            print(self.param)
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
        yield {
                'connect':list(product(address,port)),
                'timeout':timeout,
                'flag':flag
                }

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
            self.tcping_P=None
            self.ping_P=None
            self.excute_ssh_cmd_P=None
            self.get_ssh_shell_P=None

    def state_change(self,next_state):
        self.var.next_state=next_state

    def tcping(self,param):
        #获取参数
        self.tcping_P=Param_Produce(param).tcping_P() 
        for tcping_p in self.tcping_P:
            connect=tcping_p['connect']
            timeout=tcping_p['timeout']
            flag=tcping_p['flag']
            #执行
            result=tcp_port_scan(connect,timeout)
            if 'open' in flag:
                print(result['open'] or 'there are no open ports')
            if 'close' in flag:
                print(result['close'] or 'there are no close ports')
  
    def ping(self,param):
        #重置ping的历史记录
        var.ping_open=None
        var.ping_close=None  
        
        #获取参数
        self.ping_P=Param_Produce(param).ping_P() 
        
        for p in self.ping_P:
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

    def get_ssh_shell(self,param):
        #获取参数
        self.get_ssh_shell_P=Param_Produce(param).get_ssh_shell_P() 
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
        self.excute_ssh_cmd_P=Param_Produce(param).excute_ssh_cmd_P()+'\n' 
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
    