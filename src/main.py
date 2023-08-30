from ply.lex import lex
from ply.yacc import yacc
tokens=(
'ACTION',
'SN',
'OBJ',
'INNER_PARAM',
'OPRATE',
'WHERE',

)
def t_ACTION(t):
    r'(create|delete|update|select|excute)'
    return t
def t_OBJ(t):
    r'(connect|command)'
    return t
def t_WHERE(t):
    r'where'
    return t
def t_OPRATE(t): 
    r'(=>|\+|\-|\*|\/|>=|<=|=|!|/|~)'
    return t
def t_INNER_PARAM(t):
    r'(ip|port|type|protocol)'
    return t
def t_SN(t):
    r'[\u4e00-\u9fa5_a-zA-Z0-9]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

lexer=lex()

# def test(data):
#     lexer.input(data)
#     while True:
#         tok = lexer.token()
#         if not tok: 
#             break     
#         print(tok)
def p_loop(p):
    '''loop : 
    
    
    '''
def p_objexp(p):
    '''objexp : ACTION SN OPRATE OBJ
            | ACTION SN param OPRATE OBJ
            | ACTION SN WHERE OPRATE OBJ
            | ACTION SN WHERE param OPRATE OBJ
            | ACTION SN param WHERE param OPRATE OBJ
    '''
    if len(p)==4:
        p[0]=f'{p[1]} {p[2]} => {p[4]} '
        return p[0]
    
def p_param(p):
    '''param : INNER_PARAM OPRATE SN
             | INNER_PARAM OPRATE SN param
    '''
    if p[2] in ['='] :
        p[0]=f'{p[1]} = {p[3]}'

def p_error(p):
    print(f'Syntax error at {p.value!r}')

parser=yacc(debug=True)
if __name__ =='__main__':
    while True:
        try:
            s = input('[test]')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)
    # while True:
    #     s=input('[TEST]')
    #     test(s)








