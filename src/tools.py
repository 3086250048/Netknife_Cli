import socket
from concurrent.futures import ThreadPoolExecutor


#param : tagert [('192.168.2.254',443)]
def tcp_port_check(target,timeout):

     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.settimeout(timeout) 
     result = sock.connect_ex(target)
     return (result,target)
#param : flag p print r return
def tcp_port_scan(targets,timeout=1,flag="open"):
    dic={}
    open_str=''
    close_str=''
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = [executor.submit(tcp_port_check,target,timeout) for target in targets]
        for future in futures:
            result= future.result()
            if 'open' in flag:
                if result[0] == 0:
                    open_str+=f"tcp:{result[1][0]}:{result[1][1]}:open\n"
                else:
                    if 'close' in flag:
                        close_str+=f"tcp:{result[1][0]}:{result[1][1]}:close\n"
              
            if 'p' in flag:
                dic['open']=open_str.rstrip()
                dic['close']=close_str
if __name__ =='__main__':
    tcp_port_scan([['192.168.2.254','443']])





