
class Var_Error(ValueError):
    """
        Var_Error 参数错误类，规定不同报错类型对应的提示字符
    """
    def __init__(self,e_param,e_operate,e_type) -> None:
        super().__init__(self)
        self.e_param=e_param
        self.e_type=e_type
        self.e_operate=e_operate
     
        """
        :param e_param:一般情况下为报错的参数名称
        :param e_type:报错的类型,none 参数为空,notin 参数不在某个范围内(不在某个字符串列表中)\
        class 参数类型错误,range 参数超出某个范围限制(一般为数值超出),eq 参数和某个值相等
        :param e_operate:对参数进行的操作,get 取出参数时发生的错误,set 赋值时发生的错误
        """
    def __str__(self) -> str:
        return f"error:{self.e_operate}=>{self.e_param}:{self.e_type}"
    

    
    