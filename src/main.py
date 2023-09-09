ver='1.0'
from ply.lex import lex
from ply.yacc import yacc
import lexyacc.init as init


class Netknife:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Netknife, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self) -> None:
        self.lexer=lex(module=init)
        self.parser=yacc(module=init,debug=True)
        self.prompt_str='[init]'
    
    def change_state(self,file_name,prompt):
        print(id(self))
        self.lexer=lex(module=file_name)
        self.parser=yacc(module=file_name)
        self.prompt_str=prompt
        print(self.prompt_str)
    def run(self):
        print(id(self))
        while True:
            input_raw=input(self.prompt_str)
            if not input_raw:continue
            _in=input_raw.rstrip()   
            self.parser.parse(_in) 
            
         
        
    

if __name__ =='__main__':
    netknife=Netknife()
    netknife.run()

