from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
def encrypt(puk,message):
    with open(puk) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
        print("Encrypt Message: "+cipher_text.decode('utf-8'))
        return cipher_text
def decrypt(prk,message):
    with open(prk) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(message), random_generator)
        print(text.decode('utf-8'))


import re
rece_data = "ID:[A],TIME:[1637819188.150541]"
pattern = re.compile(r"^\[")
ID = re.match(pattern, rece_data)
print(ID)

