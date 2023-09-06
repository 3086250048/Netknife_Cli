ver='1.0'
from ply.lex import lex
from ply.yacc import yacc
import lexyacc.init as init,lexyacc.send as send


lexer=lex(module=init,lextab='init')
parser=yacc(module=init,debug=True)
prompt_str='[init]'
while True:
    input_raw=input(prompt_str)
    if not input_raw:continue
    _in=input_raw.rstrip()    
  
  
    if _in=='exit':
        print(exit)
        break
    
    # parser.parse(input)
    
    try:
        out=parser.parse(_in)
        print(out)
        if 'ssh' in _in:
            lexer=lex(module=send)
            parser=yacc(module=send)
            prompt_str='[send]'
     
          
                
    except Exception as e:
        print('error...')

