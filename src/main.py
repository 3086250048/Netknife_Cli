ver='1.0'
from ply.lex import lex
from ply.yacc import yacc
import lexyacc.init as init
import lexyacc.send as send 
from global_var import Global_Var

class Netknife:
    def __init__(self) -> None:
       
        self.StateMAP={
            'init':init,
            'send':send,
        }
        self.PromptMap={
            'init':'[Netknife@init]#',
            'send':'[Netknife@send]#'
        }
        self.lexer=lex(module=init)
        self.parser=yacc(module=init,debug=True)
        self.var=Global_Var()
    def run(self):
        while True:

            if (self.var.current_state != self.var.next_state) and self.var.next_state :
             
                self.var.current_state=self.var.next_state
                self.prompt_str=self.PromptMap[self.var.next_state]
                self.lexer=lex(module=self.StateMAP[self.var.next_state])
                self.parser=yacc(module=self.StateMAP[self.var.next_state])

            input_raw=input(self.PromptMap[self.var.current_state])
            if not input_raw and self.var.current_state!='send':
                continue
            else:
                if input_raw:
                    _in=input_raw.rstrip()   
                    self.parser.parse(_in)
                            
                    # try:
                    #     self.parser.parse(_in) 
                    # except Exception as e:
                    #     print(e)
            
                if self.var.current_state=='send' and not input_raw:
                    self.parser.parse('enter')
          
         
        
    

if __name__ =='__main__':
    netknife=Netknife()
    netknife.run()

