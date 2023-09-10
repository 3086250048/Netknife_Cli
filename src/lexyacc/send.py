from ply.lex import lex
from ply.yacc import yacc
from handler.protocol import Protocol_Excute


handler=Protocol_Excute()

tokens=(
'CMD',
'INNER',
'AT',
'NULL',
)

def t_AT(t):
    r'@'
    return t

def t_INNER(t):
    r'(init|send)'
    return t
def t_CMD(t):
    r'.+'
    return t
def t_NULL(t):
    r'\s+'
    return t
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_cmd_exp(p):
    '''
        cmd_exp : CMD
                | CMD NULL
                | cmd_exp CMD
                | cmd_exp CMD NULL
                | AT INNER
    '''

    if len(p)==2:
            if p[1]=='enter':
                handler.excute_ssh_cmd(' ')
            else:
                p[0]=f'{p[1]}'
                handler.excute_ssh_cmd(p[0])
    if len(p)==3:
        if p[1]=='@':
            p[0]=p[2]
            handler.state_change(p[0])
        else:
            p[0]=f'{p[1]}{p[2]}'
            handler.excute_ssh_cmd(p[0])
    if len(p)==4:
        p[0]=f'{p[1]}{p[2]}{p[3]}'
        handler.excute_ssh_cmd(p[0])


def p_error(p):
    print(f'Syntax error at {p.value!r}')       

if __name__ =='__main__':
    lexer=lex()
    parser=yacc(debug=True)
    while True: 
        s = input('[test]')
        if not s: continue
        result = parser.parse(s)
        print(result)
    
        

