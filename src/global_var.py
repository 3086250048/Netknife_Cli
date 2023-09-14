class Global_Var:
    _exist=False
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance          
    def __init__(self) -> None:
        if self._exist==False:
            self._exist=True
            #命令行状态上下文参数
            self._current_state='init'
            self._next_state=None
            
            #命令行执行上下文参数
            self._ping_open=[]
            self._tcping_open=[]
            self._ssh_open=[]
            self._ping_close=[]
            self._tcping_close=[]
            self._ssh_close=[]

            #手动添加的上下文参数
            self._extend_param={}

            #根据@语法临时给协议使用的参数
            self._temp_ip_about_param={}
            self._temp_ip_list=[]
            
    @property
    def current_state(self):
        return self._current_state 
    @property
    def next_state(self):
        return self._next_state 
    @property
    def ping_open(self):
        return self._ping_open
    @property
    def tcping_open(self):
        return self._tcping_open
    @property
    def ssh_open(self):
        return self._ssh_open
    
    @property
    def ping_close(self):
        return self._ping_close
    @property
    def tcping_close(self):
        return self._tcping_close
    @property
    def ssh_close(self):
        return self._ssh_close
    @property
    def extend_param(self):
        return self._extend_param
    @property
    def temp_ip_about_param(self):
        return self._temp_ip_about_param

    @property
    def temp_ip_list(self):
        return self._temp_ip_list
    
    
    @current_state.setter
    def current_state(self,value):
        self._current_state=value
    @next_state.setter
    def next_state(self,value):
        self._next_state=value
    @ping_open.setter
    def ping_open(self,value):
        if not value:
            self._ping_open=[]
        else:
            self._ping_open.append(value)
    @tcping_open.setter
    def tcping_open(self,value):
        if not value:
            self._tcping_open=[]
        else:
            self._tcping_open.append(value)
    @ssh_open.setter
    def ssh_open(self,value):
        if not value:
            self._ssh_open=[]
        else:
            self._ssh_open.append(value)


    @ping_close.setter
    def ping_close(self,value):
        if not value:
            self._ping_close=[]
        else:
            self._ping_close.append(value)
    @tcping_close.setter
    def tcping_close(self,value):
        if not value:
            self._tcping_close=[]
        else:
            self._tcping_close.append(value)
    @ssh_close.setter
    def ssh_close(self,value):
        if not value:
            self._ssh_close=[]
        else:
            self._ssh_close.append(value)
    @extend_param.setter
    def extend_param(self,value):
        if value['ip'] not in self._extend_param:
            self.extend_param[value['ip']]={}
        self.extend_param[value['ip']][value['key']]=value['value']
    

    @temp_ip_about_param.setter
    def temp_ip_about_param(self,value):
        self._temp_ip_about_param[value['ip']]=value['param']
    
    
    @temp_ip_list.setter
    def temp_ip_list(self,value):
        self._temp_ip_list=value
    
