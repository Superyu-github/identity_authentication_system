import socket
from Crypto import Random

from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import time
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务端
s.connect(('127.0.0.1', 9999))
# 发送标识A和挑战n1
n1 =time.time()
message = f"A,{n1}"
cipher_text = encrypt("server-public.pem", message)
s.sendall(cipher_text)
print(f"Send n1: {n1}")
# 接收B发来的挑战n1和n2
raw_data = s.recv(1024)
decrypted_data = decrypt("client-private.pem", raw_data)
id ,n= re_decode(decrypted_data.decode())
print(f"Received n: {n}")
# 验证A发回来的n1
if n[0] == str(n1):
    print("n1 verified!")
    print("identity of B verified!")
    pass
else:
    print("n1 verify error")
    exit(0)
# 向B发送收到的n2
message = f"{n[1]}"
cipher_text = encrypt("server-public.pem", message)
s.sendall(cipher_text)
print(f"Send back n2: {n[1]}")

# 向B发送key
key = "1321231"
# cipher_text = encrypt("client-private.pem", key)  # 先用A的私钥加密
# cipher_text = encrypt("server-public.pem", cipher_text.decode()) # 再用B的公钥加密
s.sendall(key.encode())
print("Send key")



# 关闭 socket
s.close()
