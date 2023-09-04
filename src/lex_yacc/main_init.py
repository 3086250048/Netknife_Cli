import sys
sys.path.append('c:\\Users\\30862\\Desktop\\NetKnife_cli\\src\\handler')
from ply.lex import lex
from ply.yacc import yacc
from itertools import product
from socket import gethostbyname
from protocol_handler import Protocol_Exec

PARAM_TABLE={
    'raw_number_to_domain_block_exp':None
}
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
'COMMA',
'NULL',
)

def t_NULL(t):
    r'\s+'
    return t
def t_DOT(t):
    r'\.'
    return t
def t_COMMA(t):
    r','
    return t
def t_NOT(t):
    r'!'
    return t
def t_RANGE(t):
    r'~'
    return t
def t_MOD(t):
    r'%'
    return t
def t_EQ(t):
    r'='
    return t
def t_PROTOCOL(t):
    r'(ssh|telnet|tftp|ftp|scp|ping|tcping|arping)'
    return t
def t_INNER(t):
    r'(ip|port|user|pwd|type)'
    return t
def t_SN(t):
    r'(\d+[a-zA-Z\u4e00-\u9fa5_]+|[a-zA-Z\u4e00-\u9fa5_]+|[a-zA-Z\u4e00-\u9fa5_]+\d+|[a-zA-Z\u4e00-\u9fa5_]+\d+[a-zA-Z\u4e00-\u9fa5_]+)'
    return t
def t_NUMBER(t):
    r'\d+'
    return t
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
# precedence = (
#     ('left', 'NUMBER'),
#     ('left', 'DOT'),
# )
# def p_object_exp(p):
#     '''

#     '''

# def p_translation_exp(p):
#     '''
#       translation_exp : cisco@ax1000:show ip int b => huawei@S5170:display ip int b   
                        
#     '''

def p_protocol_exp(p):
    '''
    protocol_exp : PROTOCOL NULL address_exp
             | PROTOCOL NULL address_exp NULL param_exp
             | PROTOCOL NULL address_exp NULL port_number_block_exp
             | PROTOCOL NULL address_exp NULL port_number_block_exp NULL param_exp
    ''' 

    # if len(p)==4:
    #     Protocol_Exec().exec(protocol=p[1],address=p[3])
    # if len(p)==6:
    #     if isinstance(p[5],list) :
    #         Protocol_Exec().exec(protocol=p[1],address=p[3],port=p[5])
    # if len(p)==8:
    #     Protocol_Exec().exec()

def p_address_exp(p):
    '''
        address_exp : ipv4_exp 
                    | domain_exp
                    | address_exp NULL ipv4_exp
                    | address_exp NULL domain_exp
    '''
   
    p[0]=[]
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=p[1]+p[3]

    print(p[0])
  
def p_domain_exp(p):
    '''
        domain_exp : domain_block_exp 
                   | domain_exp COMMA domain_block_exp 
    '''
    p[0]=[]

    if  len(p)<=2:
        p[0]=[gethostbyname(p[1])]
    else:
        p[0]=p[1]+ [gethostbyname(p[3])]
    print(p[0])

def p_ipv4_exp(p):
    '''
        ipv4_exp : ipv4_number_block_exp DOT ipv4_number_block_exp DOT ipv4_number_block_exp DOT ipv4_number_block_exp
    '''
    product_ip=list(product(p[1],p[3],p[5],p[7]))
    p[0]=[".".join(i) for i in product_ip ]
   
def p_port_number_block_exp(p):
    '''
        port_number_block_exp : number_block_exp 
                            | NOT number_block_exp
                            | number_block_exp NOT number_block_exp
    '''
    leg_number=[i for i in range(1,65536)]
  
    if len(p)==2:
        p[0]=[str(i) for i in p[1] if i >=1 and i<=65535]
    if len(p)==3:
        gen_number=[i for i in p[2] if i >=1 and i<=65535]
        p[0]=[str(i) for i in leg_number if i not in gen_number]
    if len(p)==4:
        gen_number_1= [i for i in p[1] if i >=1 and i<=65535]
        gen_number_2= [i for i in p[3] if i >=1 and i<=65535]
        p[0]=[str(i) for i in gen_number_1 if i not in gen_number_2]

def p_ipv4_number_block_exp(p):
    
    '''
        ipv4_number_block_exp : number_block_exp 
                            | NOT number_block_exp
                            | number_block_exp NOT number_block_exp
    '''
    leg_number=[i for i in range(0,256)]
  
    if len(p)==2:
        p[0]=[str(i) for i in p[1] if i >=0 and i<=255]
        PARAM_TABLE['raw_number_to_domain_block_exp']=p[1]
    if len(p)==3:
        gen_number=[i for i in p[2] if i >=0 and i<=255]
        p[0]=[str(i) for i in leg_number if i not in gen_number]
    if len(p)==4:
        gen_number_1= [i for i in p[1] if i >=0 and i<=255]
        gen_number_2= [i for i in p[3] if i >=0 and i<=255]
        p[0]=[str(i) for i in gen_number_1 if i not in gen_number_2]
    print(p[0])


def p_domain_block_exp(p):
    '''
        domain_block_exp : SN DOT SN
                         | ipv4_number_block_exp DOT SN
                         | domain_block_exp DOT SN
                         | domain_block_exp DOT NUMBER

    '''
    if isinstance(p[1],list):
        if PARAM_TABLE["raw_number_to_domain_block_exp"]:
            p[0]=f'{PARAM_TABLE["raw_number_to_domain_block_exp"][0]}.{p[3]}'
        
    else:
        p[0]=f'{p[1]}.{p[3]}'
    print(p[0])

def p_number_block_exp(p):
    '''
        number_block_exp : number_exp
                        | number_block_exp COMMA number_exp
    '''
    p[0]=[]
    if len(p)==2:
        p[0]=p[1]
    if len(p)==4:
        p[0]=list(set(p[1]+p[3]))
    if len(p)>4:
        i=0 
  
        while i<len(p):
            if i%2!=0:
                p[0]=list(set(p[1]+p[3]))
            i+=1 
  
def p_number_exp(p):
    '''
        number_exp : NUMBER 
                | NUMBER RANGE NUMBER
                | NUMBER RANGE NUMBER MOD NUMBER
                
    ''' 

    p[0]=[]
    if len(p)==2:
        p[0].append(int(p[1]))
    if len(p)==4:
        p[0]+=[i for i in range(int(p[1]),int(p[3])+1)]
    if len(p)==6:
        p[0]+=[i for i in range(int(p[1]),int(p[3])+1) if i % int(p[5])==0]

def p_param_exp(p):
    '''
        param_exp : INNER EQ SN
                  | INNER EQ address_exp
                  | INNER EQ port_number_block_exp
                  | INNER EQ SN NULL param_exp
                  | INNER EQ address_exp  NULL param_exp
                  | INNER EQ port_number_block_exp  NULL param_exp
                
    '''
    p[0]={}
    if len(p)==4:
        p[0][p[1]]=p[3]
    else:
        p[0]=p[5]
        p[0][p[1]]=p[3]
    print(p[0])

        

def p_error(p):
    print(f'Syntax error at {p.value!r}')

lexer=lex()
parser=yacc(debug=True)

if __name__ =='__main__':
    
    while True: 
        try:
            s = input('[test]')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)







