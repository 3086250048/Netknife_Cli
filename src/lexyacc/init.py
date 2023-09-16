from ply.lex import lex
from ply.yacc import yacc
from itertools import product
from socket import gethostbyname
from handler.protocol import Protocol_Excute
from global_var import Global_Var 
from tools import (
inner_param_print,
inner_param_get,
extend_param_get,
extend_param_print
)
from tools import  (
    init_exp__at
)


var=Global_Var()
handler=Protocol_Excute()
MAP={
    'ssh':handler.get_ssh_shell,
    'ping':handler.ping,
    'tcping':handler.tcping,
}

PARAM_TABLE={
    'raw_number_to_domain_block_exp':None
}

tokens=(
'INNER',
'EQ',
'WORD',
'PROTOCOL',
'RANGE',
'MOD',
'NUMBER',
'DOT',
'NOT',
'COMMA',
'NULL',
'AT',
'SEMICOLON'
)

def t_SEMICOLON(t):
    r';'
    return t

def t_AT(t):
    r'@'
    return t
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
    r'(ip|port|user|pwd|type|timeout|flag|retry|sort)'
    return t

def t_WORD(t):
    r'[a-zA-Z\u4e00-\u9fa5_]+'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_init_exp(p):
    '''
        init_exp : at_exp
                 | PROTOCOL NULL at_exp
                 | PROTOCOL NULL address_exp NULL at_exp
                 | PROTOCOL NULL address_exp NULL at_exp NULL param_exp
                 | PROTOCOL NULL address_exp 
                 | PROTOCOL NULL address_exp NULL param_exp
                 | PROTOCOL NULL address_exp NULL port_number_block_exp
                 | PROTOCOL NULL address_exp NULL port_number_block_exp NULL param_exp
    ''' 
    # 
    if len(p)==2:
        if  p[1]['protocol_about']:
            inner_param_print(p[1]['protocol_about'])
        if p[1]['param_about']:
            for set_dic in p[1]['param_about']:
                extend_param_print(set_dic)
        if p[1]['param_set']:
            for value in p[1]['param_set']:
                var.extend_param=value
        #这里return 防止只进行about set 操作时进行执行
        return
    p[0]={}
    if len(p)==4:
        p[0]['protocol']=p[1]
        #判断 PROTOCOL NULL at_exp | PROTOCOL NULL address_exp 这两种句型
        if isinstance(p[3],dict):
            result=init_exp__at(p[3]['protocol_about'])
            MAP[p[1]](result)
            #@语法时单独调用函数处理，return防止继续执行导致p[0]在关键key未被赋值的情况下传递
            return
        else:
            #list
            p[0]['address']=p[3]
    if len(p)==6:
        if isinstance(p[5],list):
          
            p[0]['protocol']=p[1]
            p[0]['address']=p[3]
            p[0]['port']=p[5]
        if isinstance(p[5],dict):
           
            # if :  PROTOCOL NULL address_exp NULL param_exp
            # else: PROTOCOL NULL address_exp NULL at_exp
            
            if 'protocol_about' not in p[5]:
           
                p[0]['protocol']=p[1]
                p[0]['address']=p[3]
                p[0]['param']=p[5]
            else:
           
                result=init_exp__at(p[5]['protocol_about'])
                result['address']=p[3]
                MAP[p[1]](result)
                return
    if len(p)==8:
            #if: PROTOCOL NULL address_exp NULL port_number_block_exp NULL param_exp
            #else: PROTOCOL NULL address_exp NULL at_exp NULL param_exp
            if isinstance(p[5],list):
                p[0]['protocol']=p[1]
                p[0]['address']=p[3]
                p[0]['port']=p[5]
                p[0]['param']=p[7]
            else:
                result=init_exp__at(p[5]['protocol_about'])
                result['address']=p[3]
                result['param']=p[7]
                MAP[p[1]](result)
                return
                
    # 没有@语法时正常执行
    MAP[p[1]](p[0])

def p_at_exp(p):
    '''
        at_exp : at_protocol_exp
               | at_param_exp
               | at_exp NULL at_protocol_exp
               | at_exp NULL at_param_exp
    '''
    if len(p)==2:
        '''
        由于protocol 为设定上为内置变量所以无法进行手动赋值，只能通过ping\tcping\ssh...操作被动添加
        所以没有protocol_set key,带有about后缀的key主要为get和print相关函数提供查询索引。
        '''
        p[0]={
            'protocol_about':[],
            'param_about':[],
            'param_set':[]
        }
        if isinstance(p[1],str):
            p[0]['protocol_about']=p[1].strip('@').split(',')
        if isinstance(p[1],dict):
            p[0]['param_about']=[p[1]]
        if isinstance(p[1],list):
            p[0]['param_set']=p[1]
    if len(p)==4:
        p[0]=p[1]
        if isinstance(p[3],str):
            p[0]['protocol_about']+=p[3].strip('@').split(',')
        if isinstance(p[3],dict):
            p[0]['param_about']+=[p[3]]
        if isinstance(p[3],list):
            p[0]['param_set']+=p[3]
   

def p_at_protocol_exp(p):
    '''
    at_protocol_exp : AT  
                    | AT PROTOCOL 
                    | AT NOT PROTOCOL
                    | at_protocol_exp COMMA PROTOCOL
                    | at_protocol_exp COMMA NOT PROTOCOL
    '''
    if len(p)==2:
        p[0]='all'
    if len(p)==3:
        p[0]=f'{p[1]}{p[2]}'
    if len(p)==4:
        if p[2]=='!':
            p[0]=f'{p[1]}!{p[3]}'
        if p[2]==',':
            p[0]=f'{p[1]},{p[3]}'
    if len(p)==5:
        p[0]=f'{p[1]},!{p[4]}'


def p_at_param_exp(p):
    '''
    at_param_exp : INNER AT address_exp 
                 | AT address_exp 
                 | INNER AT address_exp EQ sn_exp 
                 | INNER AT address_exp EQ NUMBER 
    '''  
    if len(p)==3:
        p[0]={
            'ip':p[2]
        }
    if len(p)==4:
        if isinstance(p[3],list):
            p[0]={
                'ip':p[3],
                'key':[p[1]]
            }    
        if isinstance(p[3],dict):
            p[0]=p[3]['key'].append(p[1])
    if len(p)==6:
            p[0]=[]
            for ip in p[3]:
                p[0].append({
                    'ip':ip,
                    'key':p[1],
                    'value':p[5],
                })


def p_address_exp(p):
    '''
        address_exp : ipv4_exp 
                    | domain_exp
                    | address_exp SEMICOLON ipv4_exp
                    | address_exp SEMICOLON domain_exp
    '''

    p[0]=[]
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=p[1]+p[3]

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
        p[0]=[i for i in p[1] if i >=1 and i<=65535]
    if len(p)==3:
        gen_number=[i for i in p[2] if i >=1 and i<=65535]
        p[0]=[i for i in leg_number if i not in gen_number]
    if len(p)==4:
        gen_number_1= [i for i in p[1] if i >=1 and i<=65535]
        gen_number_2= [i for i in p[3] if i >=1 and i<=65535]
        p[0]=[i for i in gen_number_1 if i not in gen_number_2]

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
  

def p_sn_exp(p):
    '''
        sn_exp : WORD
            | NUMBER WORD
            | sn_exp WORD
            | sn_exp NUMBER
    '''
    if len(p)==2:
        p[0]=f'{p[1]}'
    else:
        p[0]=f'{p[1]}{p[2]}'

def p_domain_block_exp(p):
    '''
        domain_block_exp : sn_exp DOT sn_exp
                        | ipv4_number_block_exp DOT sn_exp
                        | domain_block_exp DOT sn_exp
                        | domain_block_exp DOT NUMBER

    '''
    if isinstance(p[1],list):
        if PARAM_TABLE["raw_number_to_domain_block_exp"]:
            p[0]=f'{PARAM_TABLE["raw_number_to_domain_block_exp"][0]}.{p[3]}'
        
    else:
        p[0]=f'{p[1]}.{p[3]}'
    

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
        param_exp : INNER EQ sn_exp
                | INNER EQ address_exp
                | INNER EQ NULL
                | INNER EQ port_number_block_exp
                | INNER EQ sn_exp NULL param_exp
                | INNER EQ address_exp  NULL param_exp
                | INNER EQ port_number_block_exp  NULL param_exp
                
    '''
    p[0]={}
    if len(p)==4:
        if len(p[3])==1:
            p[0][p[1]]=p[3][0]
        else:
            p[0][p[1]]=p[3]
    else:
        p[0]=p[5]
        if len(p[3])==1:
            p[0][p[1]]=p[3][0]
        else:
            p[0][p[1]]=p[3]


def p_error(p):
    print(f'Syntax error at {p.value!r}')

if __name__ =='__main__':
   
 
    lexer=lex()
    parser=yacc(debug=True)
    while True: 
        s = input('[test]')
        if not s: continue
        result = parser.parse(s)







