import ply.lex as lex
tokens=(
'ACTION',
'SN',
'OBJ',
'INNER_PARAM',
'OPRATE'

)

t_ACTION=r'(create|delete|update|select)'
t_SN=r'[0-9a-zA-Z_]{1,}'
t_OBJ=r'(connect|command)'
t_INNER_PARAM=r'(ip|port|type|protocol)'
t_OPRATE=r'(\+|\-|\*|\/|=>|>=|<=|!|\||!|~)'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore  = ' \t'
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
lexer=lex.lex()

def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break     
        print(tok)

while True:
    s=input('[TEST]')
    test(s)








