import re
import time
from timeit import timeit
def cut(data,lenth):#数据按照距分组划分iv向量
    dataArr=re.findall('.{'+str(lenth)+'}',data)
    #findall函数返回字符串列表
    #匹配任意字符lenth次
    #dataArr.append(data[(len(data)*lenth):])#如果不是长度整数倍，则将剩余的划分成一个分组
    return dataArr#返回列表
#循环左移函数
def leftshift(n,k):
    k=k%32#保证在0到31位之间
    b=str(bin(n))#转化成二进制字符串
    b=b.split('0b')[1]#把0b分隔开，只要后面的字符串
    b=(32-len(b))*'0'+b#补0,直到补够32位
    return int(b[k:]+b[:k],2)#循环左移k位,然后按照二进制转化为十进制
#将字符串转化为二进制字符串且填充,然后分组
#消息填充
def fill(str):
    m=''#message
    str2=''
    for i in str:
        l=8-len((str2+bin(ord(i))).split('0b')[1])%8
        #返回对应的ASCII码值且将消息分成8bit一组
        m=m+l*'0'+(str2+bin(ord(i))).split('0b')[1]
    k=512-((64+len(m)+1))%512#填充k个0
    res=m+'1'+k*'0'#在消息m末尾后面加一个1，然后再添加k个0
    length=bin(len(m)).split('0b')[1]#计算长度并转化为二进制
    t=64-len(length)
    res=res+t*'0'+length#补充剩余的0直到64位
    res=cut(res,512)#数据分割成512一组
    return res#返回列表
def T(j):
    if(j<16):
        T=int('0x79cc4519',16)#十六进制转化为十进制
    else:
        T=int('0x7a879d8a',16)
    return T

def FF(X,Y,Z,j):
    if(j<16):
        return X^Y^Z
    else:
        return (X&Y)|(X&Z)|(Y&Z)
def GG(X,Y,Z,j):
    if(j<16):
        return X^Y^Z
    else:
        return (X&Y)|(~X&Z)
#置换函数1，式中x为字
def P0(X):
    return X^(leftshift(X,9))^(leftshift(X,17))
def P1(X):
    return X^(leftshift(X,15))^(leftshift(X,23))

#消息拓展
#压缩函数
def CF(V,B):
    #消息拓展
    W_ = []
    W = cut(B, 32)  # 32bit为一个字，512bit可以分成16个字
    for j in range(16):
        W[j] = int(W[j], 2)
   #del W[16]
    for j in range(16, 68):
        temp = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W.append(temp)
    for j in range(64):
        tmp = W[j] ^ W[j + 4]
        W_.append(tmp)
    # 初始向量是256bit,分成8个字ABCDEFGH
    reg=cut(V,8)
    for i in range(8):
        reg[i]=int(reg[i],16)#转成十进制的数字
        #这里要注意，因为应该是32bit,所以最大值是2的32次方-1,即4294967295,超过这个数都要约掉2的32次方
    for j in range(64):
        SS1=leftshift(((((leftshift(reg[0],12)+reg[4])%(2**32))+leftshift(T(j),j))%(2**32)),7)
        SS2=SS1^leftshift(reg[0],12)
        TT1=(((((FF(reg[0],reg[1],reg[2],j)+reg[3])%(2**32))+SS2)%(2**32))+W_[j])%(2**32)
        TT2=(((((GG(reg[4],reg[5],reg[6],j)+reg[7])%(2**32))+SS1)%(2**32))+W[j])%(2**32)
        reg[3]=reg[2]
        reg[2]=leftshift(reg[1],9)
        reg[1]=reg[0]
        reg[0]=TT1
        reg[7]=reg[6]
        reg[6]=leftshift(reg[5],19)
        reg[5]=reg[4]
        reg[4]=P0(TT2)
    V_=''
    V2=''
    for i in range(8):
        reg[i]=str(hex(reg[i])).split('0x')[1]#转化成十六进制的字符串
        k=8-len(reg[i])
        V_=V_+k*'0'+reg[i]#补充到8个十六进制就是32bit
    V1=int(V_,16)^int(V,16)#初始向量是256bit
    V2=hex(V1).split('0x')[1]
    if len(V2)<64:#如果不够64bit,就补充到64bit
        V2='0'*(64-len(V2))+str(V2)#补充到64bit
    return V2
#初始向量值
def Rho():
    s=[]
    start=1
    rho=0
    for i in range(10000):
        s.append(rho)
        if(rho<1000):
            rho=2*rho+1
        else:
            rho=start+1
            start+=1
    return s
result=Rho()
print(Rho())
#import timeit
starttime=time.perf_counter()
#s = 'abc'
IV0 = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
#for i in range(10000):
for  i in Rho():
    B = fill(str(i))
    for b in B:
        if b != '':
            IV = CF(IV0, b)
            #生日攻击
            ans=IV[:4]
            if(ans=='aa93'):
                print(IV)
endtime=time.perf_counter()
runtime=endtime-starttime
print(runtime)






