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
def MessageExpansion(B):
    #将消息分组B划分为16个字W0,W1,...W15
    W_=[]
    W=cut(B,32)#32bit为一个字，512bit可以分成16个字
    for j in range(16):
        W[j]=int(W[j],2)
    for j in range(16,68):
        temp=P1(W[j-16]^W[j-9]^leftshift(W[j-3],15))^(leftshift(W[j-13],7))^W[j-6]
    W.append(temp)
    for j in range(64):
        tmp=W[j]^W[j+4]
        W_.append(tmp)
    return W_#返回值是一个十进制数字
#压缩函数
def CF(V,B):
    #消息拓展
    W_ = []
    W = cut(B, 32)  # 32bit为一个字，512bit可以分成16个字
    for j in range(16):
        W[j] = int(W[j], 2)
   #del W[16]
    W.extend([0]*(68-16))
    for j in range(16,17):
        W[j] = P1(W[j-16] ^ W[j-9] ^ leftshift(W[j-3], 15)) ^ (leftshift(W[j-13], 7)) ^ W[j-6]
        W[j+1] = P1(W[j-15] ^ W[j-8] ^ leftshift(W[j-2], 15)) ^ (leftshift(W[j-12], 7)) ^ W[j-5]
        W[j+2] = P1(W[j-14] ^ W[j-7] ^ leftshift(W[j-1], 15)) ^ (leftshift(W[j-11], 7)) ^ W[j-4]
    for j in range(19,20):
        W[j] = P1(W[j-16] ^ W[j-9] ^ leftshift(W[j-3], 15)) ^ (leftshift(W[j-13], 7)) ^ W[j-6]
        W[j+1] = P1(W[j-15] ^ W[j-8] ^ leftshift(W[j-2], 15)) ^ (leftshift(W[j-12], 7)) ^ W[j-5]
        W[j+2] = P1(W[j-14] ^ W[j-7] ^ leftshift(W[j-1], 15)) ^ (leftshift(W[j-11], 7)) ^ W[j-4]
    for j in range(22,23):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(25,26):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(28,29):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(31,32):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(34,35):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(37,38):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(40,41):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(43,44):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(46,47):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(49,50):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(52,53):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(55,56):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(58,59):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(61,62):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    for j in range(64,65):
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ leftshift(W[j - 3], 15)) ^ (leftshift(W[j - 13], 7)) ^ W[j - 6]
        W[j + 1] = P1(W[j - 15] ^ W[j - 8] ^ leftshift(W[j - 2], 15)) ^ (leftshift(W[j - 12], 7)) ^ W[j - 5]
        W[j + 2] = P1(W[j - 14] ^ W[j - 7] ^ leftshift(W[j - 1], 15)) ^ (leftshift(W[j - 11], 7)) ^ W[j - 4]
    W[67] = P1(W[51] ^ W[58] ^ leftshift(W[64], 15)) ^ (leftshift(W[54], 7)) ^ W[61]
    # 一直展开到第 68 个迭代次数
    W_.append(W[0] ^ W[4])
    W_.append(W[1] ^ W[5])
    W_.append(W[2] ^ W[6])
    W_.append(W[3] ^ W[7])
    W_.append(W[4] ^ W[8])
    W_.append(W[5] ^ W[9])
    W_.append(W[6] ^ W[10])
    W_.append(W[7] ^ W[11])
    W_.append(W[8] ^ W[12])
    W_.append(W[9] ^ W[13])
    W_.append(W[10] ^ W[14])
    W_.append(W[11] ^ W[15])
    W_.append(W[12] ^ W[16])
    W_.append(W[13] ^ W[17])
    W_.append(W[14] ^ W[18])
    W_.append(W[15] ^ W[19])
    W_.append(W[16] ^ W[20])
    W_.append(W[17] ^ W[21])
    W_.append(W[18] ^ W[22])
    W_.append(W[19] ^ W[23])
    W_.append(W[20] ^ W[24])
    W_.append(W[21] ^ W[25])
    W_.append(W[22] ^ W[26])
    W_.append(W[23] ^ W[27])
    W_.append(W[24] ^ W[28])
    W_.append(W[25] ^ W[29])
    W_.append(W[26] ^ W[30])
    W_.append(W[27] ^ W[31])
    W_.append(W[28] ^ W[32])
    W_.append(W[29] ^ W[33])
    W_.append(W[30] ^ W[34])
    W_.append(W[31] ^ W[35])
    W_.append(W[32] ^ W[36])
    W_.append(W[33] ^ W[37])
    W_.append(W[34] ^ W[38])
    W_.append(W[35] ^ W[39])
    W_.append(W[36] ^ W[40])
    W_.append(W[37] ^ W[41])
    W_.append(W[38] ^ W[42])
    W_.append(W[39] ^ W[43])
    W_.append(W[40] ^ W[44])
    W_.append(W[41] ^ W[45])
    W_.append(W[42] ^ W[46])
    W_.append(W[43] ^ W[47])
    W_.append(W[44] ^ W[48])
    W_.append(W[45] ^ W[49])
    W_.append(W[46] ^ W[50])
    W_.append(W[47] ^ W[51])
    W_.append(W[48] ^ W[52])
    W_.append(W[49] ^ W[53])
    W_.append(W[50] ^ W[54])
    W_.append(W[51] ^ W[55])
    W_.append(W[52] ^ W[56])
    W_.append(W[53] ^ W[57])
    W_.append(W[54] ^ W[58])
    W_.append(W[55] ^ W[59])
    W_.append(W[56] ^ W[60])
    W_.append(W[57] ^ W[61])
    W_.append(W[58] ^ W[62])
    W_.append(W[59] ^ W[63])
    W_.append(W[60] ^ W[64])
    W_.append(W[61] ^ W[65])
    W_.append(W[62] ^ W[66])
    W_.append(W[63] ^ W[67])
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
starttime=time.perf_counter()
s = 'abc'
IV0 = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
B = fill(s)
for b in B:
    if b != '':
        IV = CF(IV0, b)
        print(IV)
endtime=time.perf_counter()
runtime=endtime-starttime
print(runtime)
# 计时开始
#start_time = timeit.default_timer()

# 执行代码段
#exec_time = timeit.timeit(stmt=code, setup='from __main__ import fill, CF, B, IV0', number=1)

# 计时结束
#end_time = timeit.default_timer()

# 计算总运行时间
#run_time = end_time - start_time

# 打印运行时间
#print(f"代码执行时间: {run_time}秒")
#print(f"代码实际运行时间：{exec_time}秒")
