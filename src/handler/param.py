from tools import (
    classify_ip_param,
    get_temp_ip_about_param,
    sprint
)
from itertools import product
from handler.var import Global_Var
from ply.lex import lex
from ply.yacc import yacc




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
        self.var=Global_Var()

class Ssh_Param_Product(Param_Produce):
    
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
   
class Ping_Param_Product(Param_Produce):
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
        #
        self.ping_var=None
        #默认参数
        self.timeout=1.0
        self.retry=5
        self.flag='openclose'
        self.sort='forward'
        self.p_list=['timeout','retry','flag','sort']
    def completion_is_none_param(self):
        for ip,param in self.ping_var.items():
            for k,v in param.items():
                if v == None:
                    if k=='timeout':
                        self.ping_var[ip][k]=self.timeout
                    if k=='retry':
                        self.ping_var[ip][k]=self.retry
                    if k=='flag':
                        self.ping_var[ip][k]=self.flag
                    if k=='sort':
                        self.ping_var[ip][k]=self.sort
    
    def check(self):
       #判断是否存在@语法
        print(self.param)
        if 'ip' in self.param:
            if self.param['ip'] or  self.param['ip_port']\
                or self.param['ip_port_user_pwd']:
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
    
    def at_exp(self):
        if self.has_at_exp:
            self.has_at_exp=False
            get_temp_ip_about_param(self.at_exp_address,self.p_list)
            '''extend_param_get函数只是给temp_ip_about_param全局变量赋值，
                所以要从temp_ip_about_param中取值
            '''
            self.ping_var=self.var.temp_ip_about_param
            #将ping参数为none的设置为默认值
            self.completion_is_none_param()
            #将相同ping参数的IP归类到一个列表中,并提取有参数的IP   
            type_list,has_param_ip=classify_ip_param(self.ping_var)
            #筛选出没有参数的ip(只针对@protocl所得到的ip),使用默认参数执行
            no_has_param_ip=[ ip for ip in self.at_exp_address if ip not in has_param_ip]
            #没有参数的ip使用默认参数执行
            if no_has_param_ip:
                yield{
                    'address':no_has_param_ip,
                    'timeout':self.timeout,
                    'retry':self.retry,
                    'flag':self.flag,
                    'sort':self.sort
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
                        'timeout':p.get('timeout',self.timeout),
                        'retry':p.get('retry',self.retry),
                        'flag':p.get('flag',self.flag),
                        'sort':p.get('sort',self.sort)
                    }
    
    def address_exp(self):
        if self.has_address_exp:
            self.has_address_exp=False
            #next start this
            get_temp_ip_about_param(self.at_exp_address,self.p_list)
            '''extend_param_get函数只是给temp_ip_about_param全局变量赋值，
                所以要从temp_ip_about_param中取值
            '''
            self.ping_var=self.var.temp_ip_about_param
            #将ping参数为none的设置为默认值
            self.completion_is_none_param()
            # next start this
            param=self.param.get('param',{
                'timeout':self.timeout,
                'retry':self.retry,
                'flag':self.flag,
                'sort':self.sort
            })
            return {
                'address':self.param.get('address'),
                'timeout':param.get('timeout',self.timeout),
                'retry':param.get('retry',self.retry),
                'flag':param.get('flag',self.flag),
                'sort':param.get('sort',self.sort)
                }
    
    def result(self):
        self.check()
        ping_p=[]
        result=self.address_exp()
        if result:
            ping_p.append(result)
        for p in self.at_exp():
            ping_p.append(p)
        return ping_p
        
class Tcping_Param_Product(Param_Produce): 
    '''
        return : {
            'connect':[('address':str,'port':int),...],
            'timeout':int,
            flag:'str'
        }
    '''
    def __init__(self, param) -> None:
        super().__init__(param)
        #句型判断
        self.has_address_exp=False
        self.has_lack_port_address_exp=False
        self.has_at_ping_exp=False
        self.has_at_tcping_exp=False
        self.has_at_ssh_exp=False
        #句型所生成的tcping_type列表
        self.type_list=None
        #类中要使用的参数
        self.tcping_var=None
        self.address=[]
        self.ip_port_dict={}
        self.get_param=['port','timeout','flag']
        #默认参数
        self.timeout=1
        self.flag='openclose'
    
    def completion_lack_port_ip(self):
        #缺少port的ip列表
        lack_port_ip=[{k:v} for k,v in self.tcping_var.items() if not v['port']]
        print(f'lack_port_ip=>{lack_port_ip}')
        while lack_port_ip:
            #给other_in赋值然后进行解析，从而间接给缺少port的ip赋值
            self.var.other_in=input('Enter an expression to assign:')
            if self.var.other_in:
                if not self.var.other_in:continue
                _in=self.var.other_in.rstrip()   
                self.parser.parse(_in)
            
            #重新获取赋值后的ip_param
            get_temp_ip_about_param(self.address,self.get_param)
            self.tcping_var=self.var.temp_ip_about_param
            lack_port_ip=[k for k,v in self.tcping_var.items() if not v['port']]

    def completion_is_none_param(self):
        for ip,param in self.tcping_var.items():
            for k,v in param.items():
                if v == None:
                    if k=='port':
                        self.tcping_var[ip][k]=self.ip_port_dict[ip]
                    if k=='timeout':
                        self.tcping_var[ip][k]=self.timeout
                    if k=='flag':
                        self.tcping_var[ip][k]=self.flag
        
    def ready(self):
        if 'address' in self.param:
            self.has_address_exp=True
            if 'port' not in self.param:    
                #将包含address_exp的flag置为true
                self.has_lack_port_address_exp=True
        #判断是否有@语法
        if 'ip' in self.param:
            #判断是否@ping
            if  self.param['ip']:
                self.has_at_ping_exp=True
            #判断是否@tcping
            if self.param['ip_port']:   
                self.has_at_tcping_exp=True      
            #判断是否@ssh
            if self.param['ip_port_user_pwd']:
                self.has_at_ssh_exp=True
                  
    def get(self):
        for ip_param_type in self.type_list:
            address=[ip_param['ip'] for ip_param in ip_param_type]
            yield {
                'connect':list(product(address,ip_param_type[0]['param']['port'])),
                'timeout':ip_param_type[0]['param']['timeout'],
                'flag':ip_param_type[0]['param']['flag']
            }
            address=[]

    def address_exp(self):
        if self.has_address_exp:
            self.has_address_exp=False
            if self.has_lack_port_address_exp:
                self.has_lack_port_address_exp=False
                self.address=[]  
                self.address=self.param['address']
                #获取关于缺少port信息的address_exp的ip地址对应的参数
                get_temp_ip_about_param(self.address,self.get_param)
                self.tcping_var=self.var.temp_ip_about_param
                #使ip参数中必定有port信息
                self.completion_lack_port_ip()
              
                #使ip参数中为None的参数设置为默认值
                self.completion_is_none_param()
         
                #对相同参数的ip分类到各个类型列表
                self.type_list,has_param_ip=classify_ip_param(self.tcping_var)
                #丢出结果
                for tcping_param in self.get():
                    yield tcping_param
            else:
                #有port参数
                param=self.param.get('param',{
                    'timeout':self.timeout,
                    'flag':self.flag
                })
                yield{
                    'connect':list(product(self.param['address'],self.param['port'])),
                    'timeout':param.get('timeout',self.timeout),
                    'flag':param.get('flag',self.flag)
                }
                  
    def at_ping_exp(self):
     
        if self.has_at_ping_exp:
            self.has_at_ping_exp=False
            self.address=[]
            self.address=self.param['ip']
            #获取关于ping历史记录的ip地址对应的参数
            get_temp_ip_about_param(self.address,self.get_param)
            self.tcping_var=self.var.temp_ip_about_param
            #使ip参数中必定有port信息
            self.completion_lack_port_ip()
            #使ip参数中为None的参数设置为默认值
            self.completion_is_none_param()
            #对相同参数的ip分类到各个类型列表
            self.type_list,has_param_ip=classify_ip_param(self.tcping_var)
            #丢出结果
            for tcping_param in self.get():
                yield tcping_param
    
    def at_tcping_exp(self):
        
        if self.has_at_tcping_exp:
            self.has_at_tcping_exp=False
            self.address=[]
            #获取ssh历史记录中的地址
            self.address=[connect[0] for connect in self.param['ip_port']]
            #获取ssh历史记录中的ip地址和port对应的字典
            for connect in self.param['ip_port']:
                if connect[0] not in self.ip_port_dict:
                    self.ip_port_dict[connect[0]]=[]
                self.ip_port_dict[connect[0]].append(connect[1])
       
            #获取关于tcping历史记录的ip地址对应的参数
            get_temp_ip_about_param(self.address,self.get_param)
            self.tcping_var=self.var.temp_ip_about_param
        
            #使ip参数中为None的参数设置为默认值
            self.completion_is_none_param()
       
            #对相同参数的ip分类到各个类型列表
            self.type_list,has_param_ip=classify_ip_param(self.tcping_var)
         
            #丢出结果
            for tcping_param in self.get():
                yield tcping_param
    
    def at_ssh_exp(self):
        if self.has_at_ssh_exp:
            self.has_at_ssh_exp=False
            self.address=[]
            #获取ssh历史记录中的地址
            self.address=[shell[0] for shell in self.param['ip_port_user_pwd']]
            #获取ssh历史记录中的ip地址和port对应的字典
              #获取ssh历史记录中的ip地址和port对应的字典
            for shell in self.param['ip_port_user_port']:
                if shell[0] not in self.ip_port_dict:
                    self.ip_port_dict[shell[0]]=[]
                self.ip_port_dict[shell[0]].append(shell[1])
            #获取关于ssh历史记录的ip地址对应的参数
            get_temp_ip_about_param(self.address,self.get_param)
            self.tcping_var=self.var.temp_ip_about_param
            #使ip参数中为None的参数设置为默认值
            self.completion_is_none_param()
            #对相同参数的ip分类到各个类型列表
            self.type_list,has_param_ip=classify_ip_param(self.tcping_var)
            #丢出结果
            for tcping_param in self.get():
                yield tcping_param
            
 
    def result(self):
        self.ready()
        itr_list=[
            self.address_exp,
            self.at_ping_exp,
            self.at_tcping_exp,
            self.at_ssh_exp
        ]
        result_list=[]
        for itr in itr_list:
            for result in itr():
                print(result)
                result_list.append(result)
        return result_list
        


    
