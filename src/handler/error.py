class Var_Error(ValueError):
    def __init__(self,e_param,e_operate,e_type) -> None:
        super().__init__(self)
        self.e_param=e_param
        self.e_type=e_type
        self.e_operate=e_operate
        self.err_banner={
           'current_state':{
               'none':{
                    'get':'err:current_state:返回的参数不能为空',
                    'set':'err:current_state:传入参数不能为空',
               },
               'not_in':{
                   'set':'err:current_state:传入了意外的参数'
               }  
           },
           'next_state':{
               'none':{
                    'get':'err:next_state:返回的参数不能为空',
                    'set':'err:next_state:传入参数不能为空',
               },
               'not_in':{
                   'set':'err:next_state:传入了意外的参数'
               }  
           },
           'ply':{
               'eq':{
                   'set':'err:next_state不能与current_state相等'
               }
           }
            
        }
    def __str__(self) -> str:
        return self.err_banner[self.e_param][self.e_type][self.e_operate]