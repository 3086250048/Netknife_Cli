from sys import _getframe as fun_name

def test():
    fun_n=fun_name().f_code.co_name
    return fun_n

print(test())