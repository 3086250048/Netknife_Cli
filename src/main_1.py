from ply.lex import lex
from ply.yacc import yacc
tokens=(
'INNER',
'EQ',
'SN',
'PROTOCOL',
'RANGE',
'MOD',
'NUMBER',
'DOT',
'NOT',
'COMMA'
)
def t_DOT(t):
    r'\.'
    return t
def t_COMMA(t):
    r','
    return t
def t_NOT(t):
    r'!'
    return t
def t_PROTOCOL(t):
    r'(ssh|telnet|tftp|ftp|scp)'
    return t
def t_RANGE(t):
    r'~'
    return t
def t_MOD(t):
    r'%'
    return t

def t_NUMBER(t):
    r'\d+'
    return t
def t_INNER(t):
    r'(ip|port|user|pwd|type)'
    return t
def t_EQ(t):
    r'='
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

def p_init_exp(p):
    '''
    init_exp : PROTOCOL connect_exp
             | PROTOCOL connect_exp param_exp
    '''    
def p_connect_exp(p):
    '''
    connect_exp : address_exp
                | address_exp number_exp
    '''
def p_address_exp(p):
    '''
        address_exp : ipv4_exp
                    | domain_exp
    '''
def p_domain_exp(p):
    '''
        domain_exp : DOT SN
                   | SN DOT SN
                   | DOT SN domain_exp 
                   | SN DOT SN domain_exp
    '''
def p_ipv4_exp(p):
    '''
        ipv4_exp : number_exp DOT number_exp DOT number_exp DOT number_exp
    '''
def p_number_exp(p):
    '''
        number_exp : normal_number_exp 
                   | normal_number_exp NOT normal_number_exp
    
    '''
def p_normal_number_exp(p):
    '''
        normal_number_exp : range_number_exp 
                   | comma_number_exp
                   | range_number_exp COMMA comma_number_exp
                   | comma_number_exp COMMA range_number_exp
    '''

def p_range_number_exp(p):
    '''
        range_number_exp : NUMBER
                 | NUMBER RANGE NUMBER
                 | NUMBER MOD NUMBER 
                 | NUMBER RANGE NUMBER MOD NUMBER
       
    '''
def p_comma_number_exp(p):
    '''
    comma_number_exp : NUMBER 
                   | COMMA  NUMBER 
                   | NUMBER COMMA NUMBER 
                   | COMMA NUMBER comma_number_exp 
                   | NUMBER COMMA NUMBER comma_number_exp 
    '''




def p_param_exp(p):
    '''
        param_exp : INNER EQ SN
                  | INNER EQ ipv4_exp
                  | INNER EQ number_exp
                  | INNER EQ SN param_exp
                  | INNER EQ ipv4_exp param_exp
                  | INNER EQ number_exp param_exp
    '''


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








