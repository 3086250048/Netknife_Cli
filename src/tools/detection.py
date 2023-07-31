import socket
from concurrent.futures import ThreadPoolExecutor
# # 定义需要检测的主机和端口列表
targets = [('127.0.0.1', 80), ('127.0.0.1', 443), ('192.168.1.1', 80)]*100

def tcp_port(target,timeout):
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.settimeout(timeout) 
     result = sock.connect_ex(target)
     return (result,target)

def tcp_port_scan(targets,timeout=1,flag="sr"):
    _open=[]
    _close=[]
    _open_str=''
    _close_str=''
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = [executor.submit(tcp_port,target,timeout) for target in targets]
        for future in futures:
            result= future.result()
            if 's' in flag:
                if result[0] == 0:
                    _open_str+=f"tcp:{result[1][0]}:{result[1][1]}√\n"
                else:
                    _close_str+=f"tcp:{result[1][0]}:{result[1][1]}×\n"
              
            if 'r' in flag :
                if result[0] == 0:
                    _open.append(result[1])
                else:
                    _close.append(result[1])
        if 's' in flag:
            print('open=============>')
            print(_open_str.rstrip())
            print('close============>')
            print(_close_str)
        if 'r' in flag:
            return (_open,_close)
if __name__ == '__main__':
    while True:
        data=input('>>>')
        if data=='tcp':
            tcp_port_scan(targets)
    