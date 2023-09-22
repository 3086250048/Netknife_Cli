from handler.error import Var_Error as err
from sys import _getframe as fun_name
from typing import Any,List,Dict,Tuple,NewType,Type
from ipaddress import ip_address

"""
原始Var
"""
class Common_Var:
    #手动报错
   
    """get的值为none的错误"""
    def get_err_none(self,param):
        raise err(param,'get','none')
    """get的值不在给定的可能值内的错误"""
    def get_err_notin(self,param):
        raise err(param,'get','notin')
    
    """set的值为none错误"""
    def set_err_none(self,param):
        raise err(param,'set','none')
    """set的值类型错误"""
    def set_err_class(self,param):
        raise err(param,'set','class')
    """set的值不在给定的可能值内的错误"""
    def set_err_notin(self,param):
        raise err(param,'set','notin')
    """设定的值与某个值相等的错误"""
    def set_err_eq(self,param):
        raise err(param,'set','eq')
    """设定的值不在某个范围内的错误"""
    def set_err_range(self,param):
        raise err(param,'set','range')
    
    """append的值为none的错误"""
    def append_err_none(self,param):
        raise err(param,'append','none')
    """append的值类型错误"""
    def append_err_class(self,param):
        raise err(param,'append','class')
    """append的值不在给定的可能值内的错误"""
    def append_err_notin(self,param):
        raise err(param,'append','notin')
    """append的key已经存在字典内的错误"""
    def append_err_in(self,param):
        raise err(param,'append','in')
    """append的value的长度错误"""
    def append_err_len(self,param):
        raise err(param,'append','len')
    #装饰器自动报错
    """ 检查get时的错误"""
    def check_get_err(
            check_none:bool=True,
            check_notin_attr:str=''
            ):
        """
        check_get_err  通过键入参数自动的检查被装饰的实例属性进行get时是否合规   
        
        :param check_none:get的参数为none时是否报错
        :param check_notin_attr:判断set的值是否在实例的属性中出现(if a not in obj.attr 
        这种形式的判断),没有出现报错
        """
        def outer_wapper(func):
            def wapper(self):
                v=func(self)
                """判断get的值是否为none"""
                if check_none:
                    if  not v :
                        raise err(func.__name__,'get','none')
                """判断set的值是否在可能的值内(可能的值指可迭代元素)"""
                if check_notin_attr:
                    correct_values=getattr(self,check_notin_attr)
                    if v not in correct_values:
                        raise err(func.__name__,'get','notin')
                return v
            return wapper
        return outer_wapper
    
    """检查set时的错误"""
    def check_set_err(
            check_none:bool=True,
            check_class:List[Type]=[],
            check_notin_attr:str='',
            check_eq_attr:str='',
            check_attr_eq_attr:Tuple[str,str]=None,
            check_ge:Any=None,
            check_gt:Any=None,
            check_le:Any=None,
            check_lt:Any=None,
            compare_fun:callable=None
            ):
        """
        check_set_error 通过键入参数自动的检查被装饰的实例属性进行set时是否合规    
        
        :param check_none:set的参数为none时是否报错
        :param check_class:判断set的参数是否在check_class列表内,不在时报错
        :param check_notin_attr:判断set的值是否在实例的属性中出现,(if fun_name not in obj 
        ),没有出现报错。
        :param check_eq_attr:判断set的值是否与实例的属性相等(if obj.func_name == obj.attr),相等时报错
        :param check_ge | check_gt | check_le | check_lt:判断set的值是否在
        规定的范围内,check_ge和check_le的优先级高于check_gt和check_lt,如果只
        给check_ge赋值,那么只要大于check_ge就不会报错,以此类推。
        :param check_attr_eq_attr:判断经过set操作后实例的某两个属性是否相等,相等则报错。
        :param compare_fun:将set过后的值传入compare_fun内后再进行比较。
        """
        def outer_wapper(func):
            def wapper(self,*args,**kwargs):
                fun_name=func.__name__
                cls=f'{type(self)}'
                obj_attr=f'{cls}.{fun_name}'

                excute_before_v=getattr(self,f'_{fun_name}')
                func(self,*args,**kwargs)
                excute_after_v=getattr(self,f'_{fun_name}')
                """判断set的值是否为none"""
                if check_none:
                    if not excute_after_v: 
                        setattr(self,f'_{fun_name}',excute_before_v)
                        raise err(f'{obj_attr}','set','none')
                """判断set的值class是否正确"""
                if check_class:
                    flag=False
                    for cls in check_class:
                        if  isinstance(excute_after_v,cls):flag=True
                    if not flag:
                        setattr(self,f'_{fun_name}',excute_before_v)
                        raise err(fun_name,'set','class')
                """判断set的值是否在可能的值内(可能的值指可迭代元素)"""
                if check_notin_attr:
                        if excute_after_v not in getattr(self,check_notin_attr):
                            setattr(self,f'_{fun_name}',excute_before_v)
                            raise err(fun_name,'set','notin')
                """判断set的值是否和实例上的属性冲突"""
                if check_eq_attr:
                    if excute_after_v == getattr(self,check_eq_attr):
                        setattr(self,f'_{fun_name}',excute_before_v)
                        raise err(fun_name,'set',f'{obj_attr}_eq_{cls}.{attr}')
                """判断set的值是否在规定的范围内"""
                if  check_ge or check_gt or check_le or check_lt :
                    if compare_fun:
                            excute_after_v=compare_fun(excute_after_v)
                    result_list=[]
                    if check_ge:
                        result_list.append(excute_after_v>=check_ge)
                    elif check_gt:
                        result_list.append(excute_after_v>=check_gt)
                    if check_le:
                        result_list.append(excute_after_v<=check_le)
                    elif check_lt:
                        result_list.append(excute_after_v<=check_lt)
                    for result in result_list:
                        if not result :
                            setattr(self,f'_{fun_name}',excute_before_v)
                            raise err(fun_name,'set','range')
                        
                """判断set后的实例上某两个属性是否相等"""
                if check_attr_eq_attr:
                    for attr in check_attr_eq_attr:
                        if not isinstance(attr,str) or not attr:
                            setattr(self,f'_{fun_name}',excute_before_v)
                            raise err(fun_name,'check_set_error_inner_check_none','none')
                    if not hasattr(self,check_attr_eq_attr[0]) or not hasattr(self,check_attr_eq_attr[1]):
                        setattr(self,f'_{fun_name}',excute_before_v)
                        raise err(fun_name,'check_set_error_inner_check_notin','notin')
                    if getattr(self,check_attr_eq_attr[0]) == getattr(self,check_attr_eq_attr[1]):
                        setattr(self,f'_{fun_name}',excute_before_v)
                        raise err(fun_name,'set',f'{cls}.{check_attr_eq_attr[0]}_eq_{cls}.{check_attr_eq_attr[1]}')
            return wapper
        return outer_wapper
    
"""
局部Var
"""
class Number_Var(Common_Var):
    """
        Number_Var 用于检查CLI中的数字类型变量以及保存返回操作
    
        :param timeout:超时时间
        :param retry:重式次数
        :param port:端口号
    """
    def __init__(self) -> None:
      
        self._timeout=0
        self._retry=0
        self._port=0

    @property
    @Common_Var.check_get_err(check_none=True)
    def timeout(self)-> int | float:
        return self._timeout
    
    @timeout.setter
    @Common_Var.check_set_err(check_none=True,check_class=[int,float])
    def timeout(self,timeout:int | float)->None:
        self._timeout=timeout
    
    @property
    @Common_Var.check_get_err(check_none=True)
    def retry(self)->int:
        return self._retry
    
    @retry.setter
    @Common_Var.check_set_err(check_none=True,check_class=[int])
    def retry(self,retry_count:int):
        self._retry=retry_count
    
    @property
    @Common_Var.check_get_err(check_none=True)
    def port(self)->int:
        return self._port
    
    @port.setter
    @Common_Var.check_set_err(check_none=True,check_class=[int],check_ge=1,check_le=65535)
    def port(self,port:int)->None:
        self._port=port

class String_Var(Common_Var):
    """
        String_Var : 用于检查CLI中的字符类型变量以及保存返回操作
        
        :param flag:控制打印参数,open为有响应的结果,close为无响应或失败的结果
        :param correct_flag:flag的可能值
        :param sort:控制打印的输出顺序
        :param correct_sort:sort的可能值
        :param pwd:用户密码
        :param user:用户名
        :param address:点分十进制地址(ipv4)
    """
    def __init__(self) -> None:
        self._flag=''
        self._correct_flag=(
            'open',
            'close',
            'all',
            'openclose'
        )
        self._sort=''
        self._correct_sort=(
            're',
            'for',
            'reverse',
            'forward',
        )
        self._pwd=''
        self._user=''
        self._address=''
        
    
    
    @property
    @Common_Var.check_get_err(check_none=True)
    def flag(self)->str:
        return self._flag

    @flag.setter
    @Common_Var.check_set_err(check_none=True,check_class=[str],check_notin_attr='_correct_flag')
    def flag(self,flag:str)->None:
        self._flag=flag

    @property
    @Common_Var.check_get_err(check_none=True)
    def sort(self)->str:
        return self._sort

    @sort.setter
    @Common_Var.check_set_err(check_none=True,check_class=[str],check_notin_attr='_correct_sort')
    def sort(self,sort:str):
        self._sort=sort

    @property
    @Common_Var.check_get_err(check_none=True)
    def pwd(self) -> str:
        return self._pwd

    @pwd.setter
    @Common_Var.check_set_err(check_none=True,check_class=[str])
    def pwd(self,pwd:str) -> str:
        self._pwd=pwd

    @property
    @Common_Var.check_get_err(check_none=True)
    def user(self) -> str:
        return self._user

    @user.setter
    @Common_Var.check_set_err(check_none=True,check_class=[str])
    def user(self,user:str)-> None:
        self._user=user

    @property
    @Common_Var.check_get_err(check_none=True)
    def address(self) -> str:
        return self._address

    @address.setter
    @Common_Var.check_set_err(
        check_none=True,
        check_class=[str],
        check_ge=ip_address('0.0.0.0'),
        check_le=ip_address('255.255.255.255'),
        compare_fun=ip_address
        )
    def address(self,address:str)->None:
        self._address=address

class List_Var(Common_Var):
    """
        List Var 用于保存列表类型的数据,以及列表列表数据的检查、返回、限制。

        :param ports:数组列表
        :param addresses:地址列表
        :param connects:(地址,端口)列表
        :param shells:(地址,端口,用户,密码)列表
    """
    def __init__(self) -> None:
        self.number_var=Number_Var()
        self.string_var=String_Var()
        self._ports=[]
        self._addresses=[]
        self._connects=[]
        self._shells=[]
    

    """
        Ports
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def ports(self) -> List[int]:
        return self._ports
    
    @ports.setter
    @Common_Var.check_set_err(check_none=True)
    def ports(self,ports:List[int])->None:
        self._ports=[]
        for port in ports:
            self.number_var.port=port
            self._ports.append(self.number_var.port)
    
    def ports_append(self,port:int)->None:
        self.number_var.port=port
        self._ports.append(self.number_var.port)
        
    def ports_pop(self)->int | None:
        if not self._ports: return None
        return self._ports.pop()
    
    def ports_reset(self)->None:
        self._ports=[]
    """
        Addresses
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def addresses(self):
        return self._addresses
    
    @addresses.setter
    @Common_Var.check_set_err(check_none=True)
    def addresses(self,addresses:List[str])->None:
        self._addresses=[]
        for address in addresses:
            self.string_var.address=address
            self._addresses.append(self.string_var.address)

    def addresses_append(self,address:str)->None:
        self.string_var.address=address
        self._addresses.append(self.string_var.address)

    def addresses_pop(self)->str | None:
        if not self._addresses:return None
        return self._addresses.pop()

    def addresses_reset(self)->None:
        self._addresses=[]
    """
        Connects
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def connects(self)->List[Tuple[str,int]]:
        return self._connects
    
    @connects.setter
    @Common_Var.check_set_err(check_none=True)
    def connects(self,connects:List[Tuple[str,int]])->None:
        fun_n=fun_name().f_code.co_name
        self._connects=[]
        for connect in connects:  
            if not len(connect)==2:self.append_err_len(fun_n)
            self.string_var.address=connect[0]
            self.number_var.port=connect[1]
            self._connects.append((self.string_var.address,self.number_var.port))
    
    def connects_append(self,connect:Tuple[str,int])->None:
        fun_n=fun_name().f_code.co_name
        if not len(connect)==2:self.append_err_len(fun_n)
        self.string_var.address=connect[0]
        self.number_var.port=connect[1]
        self._connects.append((self.string_var.address,self.number_var.port))

    def connects_pop(self)-> Tuple[str,int] | None:
        if not self._connects:return None
        return self._connects.pop()
    
    def connects_reset(self)->None:
        self._connects=[]
    """
        Shells
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def shells(self)->List[Tuple[str,int,str,str]]:
        return self._shells
    
    @shells.setter
    @Common_Var.check_set_err(check_none=True)
    def shells(self,shells:List[Tuple[str,int,str,str]])-> None:
        fun_n=fun_name().f_code.co_name
        self._shells=[]
        for shell in shells:
            if not len(shell)==4:self.append_err_len(fun_n)
            self.string_var.address=shell[0]
            self.number_var.port=shell[1]
            self.string_var.user=shell[2]
            self.string_var.pwd=shell[3]
            self._shells.append((
            self.string_var.address,
            self.number_var.port,
            self.string_var.user,
            self.string_var.pwd
            ))
    
    def shells_append(self,shell:Tuple[str,int,str,str])->None:
        fun_n=fun_name().f_code.co_name
        if not len(shell)==4:self.append_err_len(fun_n)
        self.string_var.address=shell[0]
        self.number_var.port=shell[1]
        self.string_var.user=shell[2]
        self.string_var.pwd=shell[3]
        self._shells.append((
        self.string_var.address,
        self.number_var.port,
        self.string_var.user,
        self.string_var.pwd
        ))

    def shells_pop(self)->Tuple[str,int,str,str] | None:
        if not self._shells:return None
        return self._shells.pop()
    
    def shells_reset(self)->None:
        self._shells=[]


"""
单例元类
"""
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
"""
全局Var
"""

class State_Var(Common_Var,metaclass=Singleton):
    """
            State_Var 用于存储CLI界面的ply状态,状态的切换,状态的查询
   
            :param current_state:CLI当前状态
            :param next_state:CLI即将要切换的状态
            :param states:所有状态列表
            :param prompts:状态对应的提示符
            :param prompt:当前的提示符
            :param plys:状态对应的lexyacc文件
            :param ply:当前所使用的ply
    """
       
    
    def __init__(self,
                 plys:Dict[str,object],
                 current_state:str,
                 prompts:Dict[str,str],
                 ) -> None:
            
            self._current_state=current_state
            self._next_state=''
            self._prompts=prompts
            self._plys=plys
            self._states=tuple(self._plys)
            self._ply=self._plys[self._current_state]
            self._prompt=self._prompts[self.current_state]
            
        

    @property
    @Common_Var.check_get_err(check_none=True)
    def current_state(self)->str:
        return self._current_state
    
    @current_state.setter
    @Common_Var.check_set_err(check_none=True,check_notin_attr='_states')
    def current_state(self,state:str) -> None:
        self._current_state=state
    
    @property
    @Common_Var.check_get_err(check_none=True)
    def next_state(self) -> str:
        return self._next_state
    
    @next_state.setter
    @Common_Var.check_set_err(check_none=True,check_notin_attr='_states')
    def next_state(self,state:str) -> None:
        self.next_state=state
    
    ply_file = NewType('ply',Any)
    @property
    def ply(self)-> ply_file :
        """
        返回与current_state对应的ply文件
        """
        return self._plys[self._current_state]
  
    @ply.setter
    def ply(self,use_ply_file:str)->None:
        """
        将value赋值给next_state,如果next_state与current_state
        不相等则切换current_state和prompt
        """
        fun_n=fun_name().f_code.co_name
        if not isinstance(use_ply_file,str):self.set_err_class(fun_n)
        if use_ply_file not in self._states:self.get_err_notin(fun_n)
        self._next_state=use_ply_file
        if self._current_state == self._next_state:self.set_err_eq(fun_n)
        self._current_state=self._next_state
        self.prompt=self._prompts[self._current_state] 


class Inner_Var(Common_Var,metaclass=Singleton):
    """
    Inner_Var 通过CLI执行协议所创建的变量

    :param ping_open:执行ping命令后成功响应ping请求的地址
    :param ping_close:执行ping命令后ping请求失败的地址
    :param tcping_open:执行tcping命令后tcp端口开放的地址
    :param tcping_close:执行tcping命令后tcp端口关闭的地址
    :param ssh_open:执行ssh命令后获取ssh的shell成功的地址
    :param ssh_close:执行ssh命令后获取ssh的shell失败的地址
    
    """
    def __init__(self) -> None:
        self.exist=True
        self._ping_open=[]
        self._ping_close=[]
        self._tcping_open=[]
        self._tcping_close=[]
        self._ssh_open=[]
        self._ssh_close=[]
        self.list_var=List_Var()
        self.string_var=String_Var()
        self.number_var=Number_Var()
    
    """
        Ping_Open
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def ping_open(self)->List[str]:
        return self._ping_open
    
    @ping_open.setter
    @Common_Var.check_set_err(check_none=True)
    def ping_open(self,addresses:List[str])->None:
        self.list_var.addresses=addresses
        self._ping_open=self.list_var.addresses

    def ping_open_append(self,address:str):
        self.string_var.address=address
        self._ping_open.append(self.string_var.address)
    
    def ping_open_pop(self)->str | None:
        if not self._ping_open:return None
        return self._ping_open.pop()
        
    def ping_open_reset(self)->None:
        self._ping_open=[]
    
    
    """
        Ping_Close
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def ping_close(self) -> List[str]:
        return self._ping_close
    
    @ping_close.setter
    @Common_Var.check_set_err(check_none=True)
    def ping_close(self,addresses:List[str])->None:
        self.list_var.addresses=addresses
        self._ping_close=self.list_var.addresses

    def ping_close_append(self,address:str) -> None:
        self.string_var.address=address
        self._ping_close.append(self.string_var.address)

    def ping_close_pop(self)->str | None:
        if not self._ping_close:return None
        return self._ping_close.pop()

    def ping_close_reset(self)->None:
        self._ping_close=[]
    """
        Tcping_Open
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def tcping_open(self)->List[Tuple[str,int]]:
        return self._tcping_open
    
    @tcping_open.setter
    @Common_Var.check_set_err(check_none=True)
    def tcping_open(self,connects:List[Tuple[str,int]])->None:
        self.list_var.connects=connects
        self._tcping_open=self.list_var.connects

    def tcping_open_append(self,connect:Tuple[str,int])->None:
        self.list_var.connects_reset()
        self.list_var.connects_append(connect)
        self._tcping_open+=self.list_var.connects

    def tcping_open_pop(self)->Tuple[str,int] | None:
        if not self._tcping_open:return None
        return self._tcping_open.pop()

    def tcping_open_reset(self)->None:
        self._tcping_open=[]
    """
        Tcping_Close
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def tcping_close(self)->List[Tuple[str,int]]:
        return self._tcping_close
    
    @tcping_close.setter
    @Common_Var.check_set_err(check_none=True)
    def tcping_close(self,connects:List[Tuple[str,int]])->None:
        self.list_var.connects=connects
        self._ping_close=self.list_var.connects

    def tcping_close_append(self,connect:Tuple[str,int])->None:
        self.list_var.connects_reset()
        self.list_var.connects_append(connect)
        self._tcping_close+=self.list_var.connects

    def tcping_close_pop(self)->Tuple[str,int] | None:
        if not self._tcping_close:return None
        return self._tcping_close.pop()

    def tcping_close_reset(self)->None:
        self._tcping_close=[]
    """
    Ssh_Open
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def ssh_open(self)->List[Tuple[str,int,str,str]]:
        return self._ssh_open
    
    @ssh_open.setter
    @Common_Var.check_set_err(check_none=True)
    def ssh_open(self,shells:List[Tuple[str,int,str,str]])->None:
        self.list_var.shells=shells
        self._ssh_open=self.list_var.shells

    def ssh_open_append(self,shell:Tuple[str,int,str,str])->None:
        self.list_var.shells_reset()
        self.list_var.shells_append(shell)
        self._ssh_open+=self.list_var.shells

    def ssh_open_pop(self)->Tuple[str,int,str,str] | None:
        if not self._ssh_open:return None
        return self._ssh_open.pop()

    def ssh_open_reset(self)->None:
        self._ssh_open=[]
    """
    Ssh_Close
    """
    @property
    @Common_Var.check_get_err(check_none=True)
    def ssh_close(self)->List[Tuple[str,int,str,str]]:
        return self._ssh_close
    
    @ssh_close.setter
    @Common_Var.check_set_err(check_none=True)
    def ssh_close(self,shells:List[Tuple[str,int,str,str]])->None:
        self.list_var.shells=shells
        self._ssh_close=self.list_var.shells

    def ssh_close_append(self,shell:Tuple[str,int,str,str])->None:
        self.list_var.shells_reset()
        self.list_var.shells_append(shell)
        self._ssh_close+=self.list_var.shells

    def ssh_close_pop(self)->Tuple[str,int,str,str] | None:
        if not self._ssh_close:return None
        return self._ssh_close.pop()

    def ssh_open_reset(self)->None:
        self._ssh_close=[]


class Extend_Var(Common_Var,metaclass=Singleton):
    """
        Extend_Var 通过在CLI键入指令创建的变量
        
        :param address_param_map:以ip地址为key,对象的参数字典为value的map
    """
    def __init__(self) -> None:
        self.exist=True
        self._address_param_map={}
        self.string_var=String_Var()
        self.number_var=Number_Var()

    @property
    @Common_Var.check_get_err(check_none=True)
    def address_param_map(self)->dict[str,Dict[str,int|str]]:
        return self._address_param_map
    
    def address_param_map_get(self,address:str,param_key:str='')->Dict[str,int|str] | int | str:
        """get某个address的全部参数,或某个参数"""
        fun_n=fun_name().f_code.co_name
        if not address:self.get_err_none(fun_n)
        if address not in self._address_param_map.keys:self.get_err_notin(fun_n)
        if param_key=='':
            return self._address_param_map[address]
        else:
            if not hasattr(self.string_var,param_key):self.get_err_notin(fun_n)
            return self._address_param_map[address][param_key]

    def address_param_map_set(
            self,address:str,
            param_key:str,
            param_value:int|str|list)->None:
        """set address的某个具体参数的值"""
        fun_n=fun_name().f_code.co_name
        if not address:self.set_err_none(fun_n)
        if address not in self._address_param_map.keys():self.set_err_notin(fun_n)
        if not param_key:self.set_err_none(fun_n)
        if not hasattr(self.string_var,param_key) or not hasattr(self.number_var,param_key):self.set_err_notin(fun_n)
        if param_key not in self._address_param_map[address]:self.set_err_notin(fun_n)
        setattr(self.string_var,param_key,param_value)
        self._address_param_map[address][param_key]=getattr(self.string_var,param_key)

    def address_param_map_append(self,address:str,param_dict:Dict[str,int|str|list])->None:
        """"""
        fun_n=fun_name().f_code.co_name
        self.string_var.address=address
        if self.string_var.address not in self._address_param_map.keys():
            self._address_param_map[self.string_var.address]={}
        if not isinstance(param_dict,dict):self.append_err_class(fun_n)
        for param_name,param_value in param_dict.items():
            if not  hasattr(self.string_var,param_name) or not hasattr(self.number_var,param_name):
                self.append_err_notin(fun_n) 
            if param_name in self._address_param_map[address].keys():
                self.append_err_in(fun_n)
            setattr(self.string_var,param_name,param_value)
            self._address_param_map[address][param_name]=getattr(self.string_var,param_name)

    def address_param_map_pop(self)->Tuple[str,Dict[str,int|str|list]]:
        if not self._address_param_map : return None
        return self._address_param_map.popitem()
    
    def address_param_map_reset(self)->None:
        self._address_param_map={}


class Temp_Var(Common_Var,metaclass=Singleton):
    """
        临时变量
    """
    def __init__(self) -> None:
        pass


    
if __name__ =='__main__':
  str_var=String_Var()
  str_var.address=['1.1.1.1']