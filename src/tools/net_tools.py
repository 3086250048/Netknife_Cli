import socket
from concurrent.futures import ThreadPoolExecutor
from scapy.all import *


def tcp_port_check(target,timeout):
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.settimeout(timeout) 
     result = sock.connect_ex(target)
     return (result,target)

def tcp_port_scan(targets,timeout=1,flag="pr"):
    _open=[]
    _close=[]
    _open_str=''
    _close_str=''
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = [executor.submit(tcp_port_check,target,timeout) for target in targets]
        for future in futures:
            result= future.result()
            if 'p' in flag:
                if result[0] == 0:
                    _open_str+=f"tcp:{result[1][0]}:{result[1][1]}:open\n"
                else:
                    _close_str+=f"tcp:{result[1][0]}:{result[1][1]}:close\n"
              
            if 'r' in flag :
                if result[0] == 0:
                    _open.append(result[1])
                else:
                    _close.append(result[1])
        if 'p' in flag:
            print(_open_str.rstrip())
            print(_close_str)
        if 'r' in flag:
            return {'open':_open,'close':_close}

# def udp_port_check(target,message="hello",flag="pr"):
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.sendto(message.encode(),target)

#     # 接收响应数据包
#     response, address = udp_socket.recvfrom(1024)
#     print('Received response: ', response.decode()) 

# def arp_check(target,timeout):
#     arp_pkt = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=target_ip)

#     # 发送ARP请求，并等待响应
#     ans, unans = srp(arp_pkt, timeout=2, verbose=False)

#     # 处理收到的ARP响应
#     for pkt in ans:
#         target_mac = pkt[1].hwsrc
#         print(f'IP: {target_ip}\tMAC: {target_mac}')

# def route_check(target,timeout):
#     pass

# def arp_check(target):
#     pass





# if __name__ == '__main__':
#     udp_port_check(('8.8.8.8',53))
#     #定义需要检测的主机和端口列表
#     # targets = [('127.0.0.1', 80)]
#     # r=tcp_port_scan(targets,flag='pr')
#     # print(r['open'])


# import argparse
# from scapy.all import *

# def arp_scan(target_ip):
#     # 创建ARP请求数据包
#     arp_pkt = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=target_ip)

#     # 发送ARP请求，并等待响应
#     ans, unans = srp(arp_pkt, timeout=2, verbose=False)

#     # 处理收到的ARP响应
#     for pkt in ans:
#         target_mac = pkt[1].hwsrc
#         print(f'IP: {target_ip}\tMAC: {target_mac}')

if __name__ == '__main__':
    pass
    