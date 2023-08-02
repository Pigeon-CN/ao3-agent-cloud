import subprocess
import time
import ipaddress
import random
import os
ip_list = []  # 用于存储 IP 的列表
prefixs = ['2001:470:c:10f:afba::','2001:470:c:10f:faba::','2001:470:c:10f:908a::','2001:470:c:10f:9515::','2001:470:c:10f:acdb::']
containers = {}  # 用于存储容器信息的字典，key 为 i，value 包含 host_port、ip 和 time
init=True
os.system("sh /root/ao3-proxy-v6/rm.sh")
def create_docker_container(i):
    """
    创建 Docker 容器的函数
    """
    host_port = 61000 + i  # 根据 i 计算 host_port 的值
    v = random.randint(0,len(prefixs)-1)
    ip = generate_ip(v)
    if(init!=True):
        prev_ip = containers[i]['ip']
        ip_list.remove(prev_ip)
    ip_list.append(ip)
    container_name = f"ao3-proxy-{i}"
    
    command = f"docker run -d -p {host_port}:80 --network=ao3-proxy-{v} --ip6='{ip}' --name '{container_name}' ao3-proxy-v6:v2"
    subprocess.run(command, shell=True)
    if(init==True):
        containers[i] = {
            "host_port": host_port,
            "ip": ip,
            "time": time.time()+random.randint(0,300)
        }
    else:
        containers[i] = {
            "host_port": host_port,
            "ip": ip,
            "time": time.time()
        }
    t1me =containers[i]["time"]
    print(f"已创建容器 {container_name}，host_port: {host_port}，ip: {ip}, time: {t1me}")
    
def remove_docker_coontainer(i):
    container_name = f"ao3-proxy-{i}"
    command = f"docker stop {container_name} && docker rm {container_name}"
    os.system(command) 
def update_ip():
    """
    更新 IP 的函数
    """
    for i in containers:
        container = containers[i]
        if time.time() - container["time"] >= 60:  # 30 分钟的时间差为 1800 秒
            remove_docker_coontainer(i)
            time.sleep(1)
            create_docker_container(i)

def generate_ip(v):
    """
    生成并返回一个不在 ip_list 中的 IP
    """
    while True:
        sub = generate_hex_random(4)
        ip = ipaddress.IPv6Address(prefixs[v]+sub)
        if ip not in prefixs:
            for i in prefixs:
                if ip != ipaddress.IPv6Address(i+"1"):
                    return ip
            
            
def generate_hex_random(length):
    """
    生成指定位数的随机16进制数
    """
    hex_chars = "0123456789ABCDEF"
    return ''.join(random.choice(hex_chars) for _ in range(length))
    
# 主程序循环创建容器和更新 IP
for i in range(300):
    create_docker_container(i)
    time.sleep(1)  # 每次创建容器后等待 1 秒
init = False
while True:
    update_ip()
    time.sleep(30)
