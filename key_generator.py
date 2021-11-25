from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)

# Server的秘钥对的生成
private_pem = rsa.exportKey()
with open("server-private.pem", "w") as f:
    f.write(private_pem.decode())

public_pem = rsa.publickey().exportKey()
with open("server-public.pem", "w") as f:
    f.write(public_pem.decode())

# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)
# Client的秘钥对的生成
private_pem = rsa.exportKey()
with open("client-private.pem", "w") as f:
    f.write(private_pem.decode())

public_pem = rsa.publickey().exportKey()
with open("client-public.pem", "w") as f:
    f.write(public_pem.decode())