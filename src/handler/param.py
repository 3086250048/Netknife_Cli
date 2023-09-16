from tools import (
    classify_ip_param,
    get_temp_ip_about_param
)
from itertools import product
from global_var import Global_Var
from ply.lex import lex
from ply.yacc import yacc
import _ply.init_state as init
var=Global_Var()


class Param_Error(ValueError):
    def __init__(self,error) -> None:
        super().__init__(self)
        self.error=error
    def __str__(self) -> str:
        return self.error


class Param_Produce:
    def __init__(self,param) -> None:
        self.param=param
        #这里需要ply是因为缺少参数时input输入解析需要。
        self.lexer=lex(module=init)
        self.parser=yacc(module=init,debug=True)

class SSH_Param_Product(Param_Produce):
    
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
   
class PING_Param_Product(Param_Produce):
    '''
        return:{
            address:[address:str],
            timeout:float,
            retry:int,
            flag:str,
            sort:str
        }
    '''
    def __init__(self, param) -> None:
        super().__init__(param)
        self.at_exp_address=[]
        self.address_exp_address=[]
        self.has_address_exp=False
        self.has_at_exp=False
    
    def ping_P_check(self):
        #判断ping @protocol 部分的ip是否超出限制
        if 'ip' in self.param or 'ip_port' in self.param\
            or 'ip_port_user_pwd' in self.param:
           #存在 protocol [adress_exp] @protocol ....句子
            self.has_at_exp=True
            self.at_exp_address=[ip for ip in self.param['ip']]+\
            [connect[0] for connect in self.param['ip_port']]+\
            [shell[0] for shell in self.param['ip_port_user_pwd']]
            if len(self.at_exp_address)>65535:
                raise Param_Error(
                        'cannot send icmp echo request to more \
                than 65535 addresses at the same time.')
        #判断ping x.x.x.x 部分的ip是否超出限制
        if 'address' in self.param : 
            #存在protocol address_exp [@protocol]....句子
            self.has_address_exp=True
            self.address_exp_address=self.param['address']
            if len(self.address_exp_address)>65535:
                raise Param_Error(
            'cannot send icmp echo request to more \
than 65535 addresses at the same time.')
    
    def at_exp_ping_P(self):
        #检查句型和ping的ip数量是否超出限制
        self.ping_P_check()
        if self.has_at_exp:
            p_list=['timeout','retry','flag','sort']
            get_temp_ip_about_param(self.at_exp_address,p_list)
            '''extend_param_get函数只是给temp_ip_about_param全局变量赋值，
                所以要从temp_ip_about_param中取值
            '''
            ping_var=var.temp_ip_about_param
            #将相同ping参数的IP归类到一个列表中,并提取有参数的IP   
            type_list,has_param_ip=classify_ip_param(ping_var)
            #筛选出没有参数的ip(只针对@protocl所得到的ip),使用默认参数执行
            no_has_param_ip=[ ip for ip in self.at_exp_address if ip not in has_param_ip]
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
    
    def address_exp_ping_P(self):
        self.ping_P_check()
        if self.has_address_exp:
            if 'param' not in self.param:self.param['param']={}
            return {
                'address':self.param.get('address'),
                'timeout':self.param['param'].get('timeout',1.0),
                'retry':self.param['param'].get('retry',5),
                'flag':self.param['param'].get('flag','openclose'),
                'sort':self.param['param'].get('sort','forward')
                }
    
    def ping_P(self):
        ping_p=[self.address_exp_ping_P()]
        for p in self.at_exp_ping_P():
            ping_p.append(p)
        return ping_p
        
class TCPING_Param_Product(Param_Produce): 
    
    def tcping_P_check(self):
        if 'port' not in self.param:
        #   raise Param_Error('the port parameter cannot be missing')
            port=[]
            wait_scan_ip=self.param['address']
            print(f'wait_scan_ip=>{wait_scan_ip}')
            port.append(int(input('port:')))
            self.param['port']=port
            print(self.param)

    def only_ip_tcping_P(self):
        '''
        return : {
            'connect':[('address':str,'port':int),...],
            'timeout':int,
            flag:'str'}
        '''
        #@协议中包含ping时的处理逻辑
        if 'ip' in self.param:
            #要get的ip
            address=self.param['ip']
            #要get的参数
            p_list=['timeout','flag','port']
            #将get到的结果给temp_ip_about_param赋值
            get_temp_ip_about_param(address,p_list)
            #重新赋到tcping_var上
            tcping_var=var.temp_ip_about_param
            print(f'149行:{tcping_var}')
           
            while True:
                lack_port_ip=[]
                for k,v in tcping_var.items():
                    if 'port' not in v or not v['port']:
                        lack_port_ip.append({k:v})
                print(f'lack_port_ip=>{lack_port_ip}')
                #给other_in赋值然后进行解析，从而间接给缺少port的ip赋值
                var.other_in=input('Enter an expression to assign:')
                if var.other_in:
                    if not var.other_in:continue
                    _in=var.other_in.rstrip()   
                    self.parser.parse(_in)
                #每次给缺少port的ip赋值后，重新获取一下缺少port参数的ip
                get_temp_ip_about_param(address,p_list)
                tcping_var=var.temp_ip_about_param
                #当没有缺少port参数的ip时则获取最新的tcping_var后退出
                if not lack_port_ip :
                    get_temp_ip_about_param(address,p_list)
                    tcping_var=var.temp_ip_about_param
                    break
            #将相同ping参数的IP归类到一个列表中,并提取有参数的IP   
            type_list,has_param_ip=classify_ip_param(tcping_var)
            #有参数的ip,则按照参数进行分组后的列表进行分别执行
            print(type_list)
            for type_p in type_list:
                connect=[]
                param=type_p[0]['param']
                for p in type_p:
                    connect.append((p['ip'],p['param']['port']))
                yield{
                    'connect':connect,
                    'timeout':param.get('timeout',1),
                    'flag':param.get('flag','openclose')
                }

    def has_ip_port_tcping_P(self):

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
                'connect':ip_port,
                'timeout':timeout,
                'flag':flag,    
            }

    def address_port_exp(self): 
      
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
