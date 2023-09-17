import socket
from concurrent.futures import ThreadPoolExecutor
from multiping import multi_ping
import socket
from global_var import Global_Var 
import paramiko
import time

'''
公共变量
'''
var=Global_Var()


def sprint(str,line):
    s=f'''
{line}>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}
{str}
{line}>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}>>>>>>>>>>>>>{line}
'''
    print(s)

class Tools_Error(ValueError):
    def __init__(self,error) -> None:
        super().__init__(self)
        self.error=error
    def __str__(self) -> str:
        return self.error


'''
上下文参数相关函数
'''
def inner_param_print(p):
    INNER_P={
    'ping':var.ping_open,
    '!ping':var.ping_close,
    'tcping':var.tcping_open,
    '!tcping': var.tcping_close,
    'ssh':var.ssh_open,
    '!ssh':var.ssh_close
    }
    if p[0]=='all':
        for key,value in INNER_P.items():
            print(f'{key}=>{value}')
    else:
        for key,value in INNER_P.items():
            if key in p:
                print(f"{key}=>{value}")

def inner_param_get(p):
    INNER_P={
    'ping':var.ping_open,
    '!ping':var.ping_close,
    'tcping':var.tcping_open,
    '!tcping': var.tcping_close,
    'ssh':var.ssh_open,
    '!ssh':var.ssh_close
    }
    result_dict={}
    for key,value in INNER_P.items():
        if key in p:
            result_dict[key]=value
    return result_dict

def extend_param_print(p):
    EXTEND_P=var.extend_param
    if 'key' not in p :
        for key,value in EXTEND_P.items():
            if key in p['ip']:
                print(f'{key}=>')
                for k,v in value.items():
                    print(f'{k}:{v}')
    else:
        for key,value in EXTEND_P.items():
            if key in p['ip']:
                print(f'{key}=>')
                for k,v in value.items():
                    if k in p['key']:
                        print(f'{k}:{v}')
'''
p :{'ip':['1.1.1.1',...],'key':['user'....]}
'''
def extend_param_get(p):
    #get如果取的ip没有赋值过属性，或指定获取的属性没有被赋值过则置为None
    EXTEND_P=var.extend_param
    for ip in p['ip']:
        if ip not in list(EXTEND_P.keys()):
            param={}
            for k in p['key']:
                param[k]=None
            var.temp_ip_about_param={'ip':ip,'param':param}
        else:
            param=EXTEND_P[ip]
            for k in p['key']:
                if k not in list(param.keys()):
                    param[k]=None
            var.temp_ip_about_param={'ip':ip,'param':param}

    #重新取赋值过None的extend_param
    EXTEND_P=var.extend_param

    if 'key' not in p :
        for key,value in EXTEND_P.items():
            if key in p['ip']:
                var.temp_ip_about_param={
                    'ip':key,
                    'param':value
                }
    else:
        for key,value in EXTEND_P.items():
            if key in p['ip']:
                param_dic={}
                for k,v in value.items():
                    if k in p['key']:
                        param_dic[k]=value[k]
                var.temp_ip_about_param={
                    'ip':key,
                    'param':param_dic
                }
'''
以下是protocol.py文件依赖函数
'''

def get_temp_ip_about_param(address,p_list):
    # 重置临时ip相关参数字典
    var.temp_ip_about_param=None
    #给temp_ip_about_param赋值
    extend_param_get({
        'ip':address,
        'key':p_list
    })

def classify_ip_param(protocol_var):
    has_param_ip=[]
    type_list=[[]]
    #对@protocol中所选中的ip按照参数进行分类
    if protocol_var:   
        for key,value in protocol_var.items():
            if not type_list[0]:
                type_list[0].append({'ip':key,'param':value})
                has_param_ip.append(key)
                continue
            append=True
            for type_p in type_list:
                if value == type_p[0]['param']:
                    append=False
                    type_p.append({'ip':key,'param':value})
                    has_param_ip.append(key)
            if append:
                type_list.append([{'ip':key,'param':value}])
                has_param_ip.append(key)
    return type_list,has_param_ip

def tcp_port_check(target,timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout) 
    result = sock.connect_ex(target)
    return (result,target)

def tcp_port_scan(targets,timeout=1):
    dic={}
    open_str=''
    close_str=''
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = [executor.submit(tcp_port_check,target,timeout) for target in targets]
        #重置tcping的历史记录
        var.tcping_open=None
        var.tcping_close=None

        for future in futures:
            result= future.result()
            if result[0] == 0:
                #添加tcping记录
                var.tcping_open=(result[1][0],result[1][1])
                open_str+=f"tcp:{result[1][0]}:{result[1][1]}:open\n"    
            else:
                var.tcping_close=(result[1][0],result[1][1])
                close_str+=f"tcp:{result[1][0]}:{result[1][1]}:close\n"   
    dic['open']=open_str.rstrip()
    dic['close']=close_str
    return dic

#['ip'...]
def ping_scan(address,timeout,retry,sort):
        
        result={
        'open':'',
        'close':''
        }
        mp=multi_ping(address,timeout,retry)
        open=[]
        close=[]
        for i in list(mp[0].keys()):
            open.append(i)
       
        for i in mp[1]:
            close.append(i)

        if 're' in sort:
            _open=sorted(open,key=socket.inet_aton,reverse=True)
            _close=sorted(close,key=socket.inet_aton,reverse=True)
        else:
            _open=sorted(open,key=socket.inet_aton)
            _close=sorted(close,key=socket.inet_aton) 


        for i in _open:
            #添加ping记录
            var.ping_open=i
            result['open']+=f'ip:{i}:open\n'

        for i in _close:
            var.ping_close=i
            result['close']+=f'ip:{i}:close\n'
        result['open']=result['open'].rstrip()

        return result

def connect_ssh_shell(connect):
    try:
        #添加ssh记录
        var.ssh_open=connect
        ssh_client = paramiko.SSHClient()   
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh_client.connect(*connect,allow_agent=False,look_for_keys=False)
        shell=ssh_client.invoke_shell()
        return shell
    except Exception as e:
        #添加ssh记录
        var.ssh_close=connect
        print(e)

 #        
def send_ssh_command(shell,cmd):
    if not shell:
        #获取shell对象失败会到init状态
        var.next_state='init'
        raise Tools_Error('shell get fault...')
    shell.send(cmd)
    time.sleep(0.1)
    output=shell.recv(65535).decode()
    return output

'''
以下是lexyacc文件夹下文件依赖的参数处理函数
'''

def init_exp__at(at_protocol):
    result={
        'ip':[],
        'ip_port':[],
        'ip_port_user_pwd':[]
    }
    for _at_protocol in at_protocol:
        if _at_protocol=='ping' or _at_protocol=='!ping':
            result['ip']+=inner_param_get(at_protocol)[_at_protocol]
        if _at_protocol=='tcping' or  _at_protocol=='!tcping':
            result['ip_port']+=[p for p in inner_param_get(at_protocol)[_at_protocol]]
        if _at_protocol=='ssh' or _at_protocol=='!ssh':
            result['ip_port_user_pwd']+=[p for p in inner_param_get(at_protocol)[_at_protocol] ]
    return result


     

if __name__ =='__main__':
    tcp_port_scan([['192.168.2.254','443']])





