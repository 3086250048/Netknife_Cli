import socket
from concurrent.futures import ThreadPoolExecutor
from multiping import multi_ping
import socket

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
        for future in futures:
            result= future.result()
            if result[0] == 0:
                open_str+=f"tcp:{result[1][0]}:{result[1][1]}:open\n"    
            else:
                close_str+=f"tcp:{result[1][0]}:{result[1][1]}:close\n"    
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
       
        for i in _open:
            result['open']+=f'ip:{i}:open\n'
        for i in _close:
            result['close']+=f'ip:{i}:close\n'
        result['open']=result['open'].rstrip()
        return result


if __name__ =='__main__':
    tcp_port_scan([['192.168.2.254','443']])





