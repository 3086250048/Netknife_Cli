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

def extend_param_get(p):
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
            print(key,value,p)
            if key in p['ip']:
                param_dic={}
                for k,v in value.items():
                    if k in p['key']:
                        param_dic[k]=value[k]
            var.temp_ip_about_param={
                'ip':key,
                'param':param_dic
            }
    print(f'tools.py:第83行{var.temp_ip_about_param}')
'''
以下是protocol.py文件依赖函数
'''

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
    #打印测试
    print(var.tcping_open) 
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

        #重置ping的历史记录
        var.ping_open=None
        var.ping_close=None

        for i in _open:
            #添加ping记录
            var.ping_open=i
            result['open']+=f'ip:{i}:open\n'

        for i in _close:
            var.ping_close=i
            result['close']+=f'ip:{i}:close\n'
        result['open']=result['open'].rstrip()
        #打印测试
        print(var.ping_open)
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
以下为可能的函数名称
    1.状态名称__P长度__参与判断的参数类型
    2.状态名称__P长度
    3.状态名称__参与判断的参数类型
'''

def init_exp__four__dict(at_protocol,ip=True,ip_port=False,ip_user_pwd=False):
    result={
        'ip':[],
        'ip_port':[],
        'ip_port_user_pwd':[]
    }
    print(f'tools.py文件第214行{at_protocol}')
    for _at_protocol in at_protocol:
        print(_at_protocol)
        if _at_protocol=='ping' or _at_protocol=='!ping':
            result['ip']+=inner_param_get(at_protocol)[_at_protocol]
        if _at_protocol=='tcping' or  _at_protocol=='!tcping':
            if ip:
                result['ip']+=[p[0] for p in inner_param_get(at_protocol)[_at_protocol]]
            if ip_port:
                result['ip_port']+=[p for p in inner_param_get(at_protocol)[_at_protocol]]
        if _at_protocol=='ssh' or _at_protocol=='!ssh':
            if ip:
                result['ip']+=[p[0] for p in inner_param_get(at_protocol)[_at_protocol]]
            if ip_port:
                result['ip_port']+=[p[0:2] for p in inner_param_get(at_protocol)[_at_protocol]]
            if ip_user_pwd:
                result['ip_port_user_pwd']+=[p for p in inner_param_get(at_protocol)[_at_protocol] ]
        print(f'tools.py第226行:{result}')
    return result
  
        
if __name__ =='__main__':
    tcp_port_scan([['192.168.2.254','443']])





