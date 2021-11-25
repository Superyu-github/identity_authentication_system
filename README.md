# identity_authentication_system

## 网络安全实践作业，实现一个简单的身份认证系统

### 一、原理简介

本例程参考教材《计算机网络安全》（马利，姚永雷著）第86页，实现了一个基于公钥密码的双向身份认证系统

![教材配图](/picture/教材配图.png)

1. A用B的公钥对含有其标识IDA和挑战(N1)的消息加密,并发送给B。其中N1用来唯一标识本次交易。
2. B发送一条用PUA加密的消息,该消息包含A 的挑战(N1)和B产生的新挑战(N2)。因为只有B可以解密消息(1),所以消息(2)中的N1可使A确信其通信伙伴是B。
3. A用B的公钥对Nz加密﹐并返回给B,这样可使B确信其通信伙伴是A。至此,A与B实现了双向认证。
4. A选择密钥K,,并将M=E(PU, ,E(PR,,K,))发送给B。使用B的公钥对消息加密可以保证只有B才能对它解密;使用A的私钥加密可以保证只有A才能发送该消息。
5. B计算D(PUA,D(PRB,M))得到密钥。
   步骤(4)、(5)实现了对称密码的密钥分配。

### 二、例程说明

1. 本例程基于python3.8实现

2. 本例程中A为客户端，B为服务端，双方通信采用TCP方式进行，TCP通信使用python自带的socket库实现，socket编程参考了https://www.jmjc.tech/tutorial/python/52

3. 公钥密码采用RSA体制，使用了python密码库pycrypto，初次使用需要安装，安装命令为`pip install pycrypto`，编程过程中参考了https://www.cnblogs.com/lanston1/p/11875706.html

   需要注意，pycrypto库对于高版本的python支持有些许问题，编程过程中遇到异常`AttributeError module 'time' has no attribute 'clock'`，查阅资料发现，Python3.8不再支持`time.clock`，但在调用时依然包含该方法。解决方法是使用`time.perf_counter()`替换报错的`time.clock()`

4. 例程中消息的识别使用了正则表达式匹配，再书写正则表达式的过程中，发现了两个有趣的网站

   https://regex101.com/r/1Z02qx/1/

   https://jex.im/regulex/#!flags=&re=%5BA-Z%5D%7C%5Cd%2B%5C.%5Cd%2B 

   有助于理解正则表达式

5. 由于pycrypto加密长度限制，原理介绍中的(4)和(5)无法正常运行，已被注释，但是身份认证功能已经实现。

### 三、例程运行

#### 运行前检查

1. 安装pycrypto

   `pip install pycrypto`

#### 运行方式

1. 运行`key_generator.py`生成A和B的公私钥密钥对,==注意：使用高版本python运行可能报错，解决方法请查看 二、例程说明==
2. 运行`sever.py`开启服务端(B)
3. 运行`client.py`开启客户端(A)

#### 运行效果截图

1. 服务端(B)

![sever](/picture/sever.png)

2. 客户端(A)

![client](/picture/client.png)

