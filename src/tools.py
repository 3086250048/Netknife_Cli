import socket
from concurrent.futures import ThreadPoolExecutor
from multiping import multi_ping
import socket
from global_var import Global_Var 
import paramiko
import time
from pprint import pprint

var=Global_Var()

def at_obj(p,show,result):
    printlist={
        'ping':var.ping_open,
        '!ping':var.ping_close,
        'tcping':var.tcping_open,
        '!tcping': var.tcping_close,
        'ssh':var.ssh_open,
        '!ssh':var.ssh_close
    }


    if show:
        if p=='all':
           for key,value in printlist.items():
                print(f'{key}=>{value}')
        else:
            for key,value in printlist.items():
                if key in p.split(','):
                    print(f"{key}=>{value}")
    if result:
        return printlist
    

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
         
    

def send_ssh_command(shell,cmd):
            shell.send(cmd)
            time.sleep(0.1)
            output=shell.recv(65535).decode()
            return output


if __name__ =='__main__':
    tcp_port_scan([['192.168.2.254','443']])





