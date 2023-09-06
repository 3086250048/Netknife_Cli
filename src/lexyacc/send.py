from ply.lex import lex
from ply.yacc import yacc


tokens=(
'CMD',
'INNER',
'AT',
'NULL'
)

def t_AT(t):
    r'@'
    return t
def t_INNER(t):
    r'init'
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
        p[0]=f'{p[1]}'
    if len(p)==3:
        p[0]=f'{p[1]}{p[2]}'
    if len(p)==4:
        p[0]=f'{p[1]}{p[2]}{p[3]}'


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
    
        

