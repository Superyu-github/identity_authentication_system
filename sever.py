import socket
import time

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import re


def encrypt(puk, message):
    with open(puk) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
        # print("Encrypt Message: " + cipher_text.decode('utf-8'))
        return cipher_text


def decrypt(prk, message):
    with open(prk) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(message), random_generator)
        # print(text.decode('utf-8'))
        return text


def re_decode(data):
    pattern = re.compile(r"[A-Z]")
    id = re.findall(pattern, data)
    pattern = re.compile(r"\d+\.\d+")
    n = re.findall(pattern, data)
    return id, n


# socket.AF_INET (IPV4)
# socket.SOCK_STREAM (TCP)
# 创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定监听地址和端口
s.bind(("127.0.0.1", 9999))
# 设置最大允许连接数量
s.listen(3)
# 死循环，重复的处理着每个客户端的请求
while True:
    # 阻塞 每当有客户端的请求过来开始执行
    # 连接处理 （已完成三次握手）并获取资源对象 | conn 请求对象 | addr 客户端地址 ip: port
    conn, addr = s.accept()
    # 接收A发来的标识和挑战n1
    raw_data = conn.recv(1024).decode('utf-8')
    decrypted_data = decrypt("server-private.pem", raw_data)
    id , n = re_decode(decrypted_data.decode())
    print(f"Received! id: {id[0]} n1: {n[0]}")
    # 产生n2，和n1一起发回给A
    n2 = time.time()
    # 检验n1与n2时间差，大于2s视为重放攻击
    if n2-float(n[0]) > 2:
        print("Replay attack!")
        exit()
    else:
        pass
    message = f"{n[0]},{n2}"
    cipher_text = encrypt("client-public.pem", message)
    conn.sendall(cipher_text)
    print(f"Send back: n1: {n[0]} n2: {n2}")
    # 接收来自A的n2
    raw_data = conn.recv(1024).decode('utf-8')
    decrypted_data = decrypt("server-private.pem", raw_data)
    id, n = re_decode(decrypted_data.decode())
    print(f"Received! n: {n}")
    # 验证n2
    if n[0] == str(n2):
        print("n2 verified!")
        print("identity of A verified!")
        pass
    else:
        print("n2 verify error!")
        exit(0)
    # 接收来自A的密钥key
    raw_data = conn.recv(1024).decode('utf-8')
    print("Received key from A")
    print(raw_data)
    # decrypted_data = decrypt("server-private.pem", raw_data)  # 先用B的私钥解密
    # decrypted_data = decrypt("client-public.pem", decrypted_data)  # 再用A的公钥解密
    # print(decrypted_data)

    # 关闭客户端连接
    conn.close()
