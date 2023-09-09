class Global_Var:
    _exist=False
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance          
    def __init__(self) -> None:
        if self._exist==False:
            self._exist=True
            self._current_state='init'
            self._next_state=None
    @property
    def current_state(self):
        return self._current_state 
    @property
    def next_state(self):
        return self._next_state 
    @current_state.setter
    def current_state(self,value):
        self._current_state=value
    @next_state.setter
    def next_state(self,value):
        self._next_state=value