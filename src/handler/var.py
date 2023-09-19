import _ply.init_state as init
import _ply.ssh_send_state as ssh_send
from error import Var_Error as err
from sys import _getframe as fun_name


class Common_Var:
    """一般变量"""

    def set_err_none(self,param):
       raise err(param,'set','none')
    def get_err_none(self,param):
       raise err(param,'get','none')
    def set_err_class(self,param):
       raise err(param,'set','class')
    def set_err_not_in(self,param):
       raise err(param,'set','value')
    def set_error_eq(self,param):
            raise err(param,'set','eq')

class Global_Var(Common_Var):
    """
        Global_var 全局变量
    """
    exist=False
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance          
    def __init__(self) -> None:
        """
            :param exist:判断Var对象是否已经创建。
        
        """
      
class State_Var(Global_Var):
    """
            State_Var 用于存储CLI界面的ply状态,状态的切换,状态的查询
    """
    def __init__(self) -> None:
        super().__init__()
        if not self.exist:
            self.exist=True
            self.current_state='init'
            self.next_state=''
            self.states=(
                'init',
                'break',
                'ssh_send',
                'telnet_send',
                'ftp_send',
            )
            self.prompts={
                'init':'[@init]#',
                'break':'<退出current_state状态>',
                'ssh_send':'[ssh@send]#',
                'telnet_send':'[telnet@send]#',
                'ftp_send':'[ftp@send]#'
            }
            self.plys={
                'init':init,
                'ssh_send':ssh_send
            }
            self.ply=init
            self.prompt=self.prompts[self.current_state]
        
        """
            :param current_state:CLI当前状态
            :param next_state:CLI即将要切换的状态
            :param states:所有状态列表
            :param prompts:状态对应的提示符
            :param prompt:当前的提示符
            :param plys:状态对应的lexyacc文件
            :param ply:当前所使用的ply
        """


    @property
    def current_state(self):
        fun_n=fun_name().f_code.co_name
        if not self.current_state:self.get_err_none(fun_n)
        return self.current_state
    @current_state.setter
    def current_state(self,value):
        fun_n=fun_name().f_code.co_name
        if not value:self.set_err_none(fun_n)
        if value not in self.states:self.set_err_not_in(fun_n)
        self.current_state=value
    @property
    def next_state(self):
        fun_n=fun_name().f_code.co_name
        if not self.next_state:self.get_err_none(fun_n)
        return self.next_state
    @next_state.setter
    def next_state(self,value):
        fun_n=fun_name().f_code.co_name
        if not value:self.set_err_none(fun_n)
        if value not in self.states:self.set_err_not_in(fun_n)
        self.next_state=value
    @property
    def ply(self):
        """
        返回与current_state对应的ply文件
        """
        return self.plys[self.current_state]
    @ply.setter
    def ply(self,value):
        """
        将value赋值给next_state,如果next_state与current_state
        不相等则切换current_state和prompt
        """
        fun_n=fun_name().f_code.co_name
        self.next_state=value
        if self.current_state == self.next_state:self.set_error_eq(fun_n)
        self.current_state=self.next_state
        self.prompt=self.prompts[self.current_state] 

class Number_Var(Common_Var):
    """
        Number_Var 用于检查CLI中的数字类型变量以及保存返回操作
    """
    def __init__(self) -> None:
        super().__init__()
        self.timeout=0
        self.retry=0
    """
        :param timeout:超时时间
        :param retry:重式次数
    """
    
    @property
    def timeout(self):
        fun_n=fun_name().f_code.co_name
        if not self.timeout:self.get_err_none(fun_n)
        return self.timeout
    
    @timeout.setter
    def timeout(self,value):
        fun_n=fun_name().f_code.co_name
        if not value:self.set_err_none(fun_n)
        if not isinstance(value,int) or not isinstance(value,float):self.set_err_class(\
            fun_n)
        self.timeout=value
    
    @property
    def retry(self):
        fun_n=fun_name().f_code.co_name
        if not self.retry:self.get_err_none(fun_n)
        return self.retry
    
    @retry.setter
    def retry(self,value):
        fun_n=fun_name().f_code.co_name
        if not value:self.set_err_none(fun_n)
        if not isinstance(value,int) :self.set_err_class(fun_n)
        self.retry=value

class String_Var(Common_Var):
    """
        String_Var : 用于检查CLI中的字符类型变量以及保存返回操作
        
    """
    def __init__(self) -> None:
        super().__init__()
        self.flag=''
        self.correct_flag=(
            'open',
            'close',
            'all',
            'openclose'
        )
        self.sort=''
        self.correct_sort=(
            're',
            'for',
            'reverse',
            'forward',
        )
        
    """
        :param flag:控制打印参数,open为有响应的结果,close为无响应或失败的结果
        :param correct_flag:flag的可能值
        :param sort:控制打印的输出顺序
        :param correct_sort:sort的可能值
    
    """
    
    @property
    def flag(self):
        fun_n=fun_name().f_code.co_name
        if not self.flag:self.get_err_none(fun_n)
        return self.flag

    @flag.setter
    def flag(self,value):
        fun_n=fun_name().f_code.co_name
        if not self.flag:self.set_err_none(fun_n)
        if not isinstance(value,str):self.set_err_class(fun_n)
        if value not in self.correct_flag:self.set_err_not_in(fun_n)
        self.flag=value

    @property
    def sort(self):
        fun_n=fun_name().f_code.co_name
        if not self.sort:self.get_err_none(fun_n)
        return self.sort

    @flag.setter
    def sort(self,value):
        fun_n=fun_name().f_code.co_name
        if not self.sort:self.set_err_none(fun_n)
        if not isinstance(value,str):self.set_err_class(fun_n)
        if value not in self.correct_sort:self.set_err_not_in(fun_n)
        self.sort=value
    
class List_Var(Common_Var):
    def __init__(self) -> None:
        super().__init__()
        pass

class Inner_Var(Global_Var):
    def __init__(self) -> None:
        super().__init__()
    pass

class Extend_Var(Global_Var):
    def __init__(self) -> None:
        super().__init__()
        pass

class Temp_Var(Global_Var):
    def __init__(self) -> None:
        super().__init__()
        pass

   


    

    # self._current_state='init'
    # self._next_state=None
    # self._ping_open=[]
    # self._tcping_open=[]
    # self._ssh_open=[]
    # self._ping_close=[]
    # self._tcping_close=[]
    # self._ssh_close=[]
    # self._extend_param={}
    # self._temp_ip_about_param={}

    # @property
    # def current_state(self):
    #     return self._current_state 
    # @property
    # def next_state(self):
    #     return self._next_state 
    # @property
    # def ping_open(self):
    #     return self._ping_open
    # @property
    # def tcping_open(self):
    #     return self._tcping_open
    # @property
    # def ssh_open(self):
    #     return self._ssh_open
    
    # @property
    # def ping_close(self):
    #     return self._ping_close
    # @property
    # def tcping_close(self):
    #     return self._tcping_close
    # @property
    # def ssh_close(self):
    #     return self._ssh_close
    # @property
    # def extend_param(self):
    #     return self._extend_param
    # @property
    # def temp_ip_about_param(self):
    #     return self._temp_ip_about_param

    # @property
    # def temp_ip_list(self):
    #     return self._temp_ip_list
    # @property
    # def other_in(self):
    #     return self._other_in
    
    # @current_state.setter
    # def current_state(self,value):
    #     self._current_state=value
    # @next_state.setter
    # def next_state(self,value):
    #     self._next_state=value
    # @ping_open.setter
    # def ping_open(self,value):
    #     if not value:
    #         self._ping_open=[]
    #     else:
    #         self._ping_open.append(value)
    # @tcping_open.setter
    # def tcping_open(self,value):
    #     if not value:
    #         self._tcping_open=[]
    #     else:
    #         self._tcping_open.append(value)
    # @ssh_open.setter
    # def ssh_open(self,value):
    #     if not value:
    #         self._ssh_open=[]
    #     else:
    #         self._ssh_open.append(value)


    # @ping_close.setter
    # def ping_close(self,value):
    #     if not value:
    #         self._ping_close=[]
    #     else:
    #         self._ping_close.append(value)
    # @tcping_close.setter
    # def tcping_close(self,value):
    #     if not value:
    #         self._tcping_close=[]
    #     else:
    #         self._tcping_close.append(value)
    # @ssh_close.setter
    # def ssh_close(self,value):
    #     if not value:
    #         self._ssh_close=[]
    #     else:
    #         self._ssh_close.append(value)
    # @extend_param.setter
    # def extend_param(self,value):
    #     if value['ip'] not in self._extend_param:
    #         self.extend_param[value['ip']]={}
    #     param_key=value['key']
    #     param_value=value['value']
    #     class_var_map=Global_Var.class_var_map
    #     if param_key in class_var_map['number_var']:
    #         if isinstance(param_value,list):
    #             param_value=param_value[0]
    #         if isinstance(param_value,str):
    #             param_value=Var_Error("number_ver Can't be str")
    #     if param_key in class_var_map['str_var'] or param_value in class_var_map['sn_var']:
    #         if isinstance(param_value,list):
    #             param_value=str(param_value[0])
    #         else:
    #             param_value=str(param_value)
    #     if param_key in class_var_map['list_var']:
    #         if isinstance(param_value,str):
    #             param_value=Var_Error("list_ver Can't be str")
    #     self.extend_param[value['ip']][param_key]=param_value
    

    # @temp_ip_about_param.setter
    # def temp_ip_about_param(self,value):
    #     if value==None:
    #         self._temp_ip_about_param={}
    #     else:
    #         self._temp_ip_about_param[value['ip']]=value['param']
    
    
    # @temp_ip_list.setter
    # def temp_ip_list(self,value):
    #     self._temp_ip_list=value
    
    # @other_in.setter
    # def other_in(self,value):
    #     self._other_in=value