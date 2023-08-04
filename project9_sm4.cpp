#include<iostream>
#include<cmath>
#include<string>
using namespace std;
typedef string BaseType;
// 定义to_BaseType函数的别名
/* std::BaseType(*to_BaseType_alias)(int);

// 使用别名来调用to_BaseType函数
to_BaseType_alias my_to_BaseType = std::to_BaseType;
std::BaseType str = my_to_BaseType(123);
*/
BaseType tostring(int value)
{
	BaseType str;
	bool isNegative = false;    // 是否为负数

	if (value < 0) {
		value = -value;
		isNegative = true;
	}

	do {
		char digit = value % 10 + '0';
		str = digit + str;
		value /= 10;
	} while (value != 0);

	if (isNegative) {
		str = '-' + str;
	}

	return str;
}

/*BaseType tos(int x) {
	stack<char> stk;
	BaseType s;
	char tmp;
	int a; //每次的个位 
	while (x) {
		a = x % 10;
		x /= 10;
		tmp = a + '0';
		stk.push(tmp);
	}
	while (stk.size()) { //利用栈逆序 
		s += stk.top();
		stk.pop();
	}
	return s;
}*/


BaseType BinToHex(BaseType str)//二进制转换为十六进制的函数
{
	BaseType hex = "";
	int temp = 0;
	while (str.size() % 4 != 0)//如果输入的字符不是4的倍数，则在前面补充0的个数
	{
		str = "0" + str;
	}
	for (int i = 0; i < str.size(); i += 4)//这里我们假设输入的是字符是以二进制新式出现的，如"10001100"等
	{
		temp = (str[i] - '0') * 8 + (str[i + 1] - '0') * 4 + (str[i + 2] - '0') * 2 + (str[i + 3] - '0') * 1;

		if (temp < 10)//如果字符串小于10，即包含"1001":9和以下。
		{
			hex += tostring(temp);//to_BaseType函数:将数字常量转换为字符串，返回值为转换完毕的字符串
		}
		else
		{
			hex += 'A' + (temp - 10);//如果超过等于10，则要转换为字符'A'到'F',例:如字符'C',，二进制为1100，temp=12，减去10剩2，然后加上字符'A'的ASCII值65，即为67对应的ASCII值为字符'C'
		}
	}
	return hex;
}
BaseType HexToBin(BaseType str)//十六进制转化为二进制
{
	BaseType bin = "";
	BaseType table[16] = { "0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111" };//十六个字符串，相当于一个有十六个字符串的一个大数组。
	for (int i = 0; i < str.size(); i++)
	{
		if (str[i] >= 'A' && str[i] <= 'F')
		{
			bin += table[str[i] - 'A' + 10];
		}
		else
		{
			bin += table[str[i] - '0'];
		}
	}
	return bin;
}
int HexToDec(char str)//十六进制转化为十进制
{
	int dec = 0;
	if (str >= 'A' && str <= 'F')//注意单引号代表的是一个字符，但是双引号代表的是字符串
	{
		dec += (str - 'A' + 10);//举例，比如字符C的ASCII值为67，然后在这个区间，然后减去字符A所对应的ASCII值，即65，还剩2，然后加上10，即12，就是C所对应的十六进制
	}
	else
	{
		dec += (str - '0');
	}
	return dec;
}
BaseType XOR(BaseType str1, BaseType str2)//实现异或函数
{
	BaseType res1 = HexToBin(str1);
	BaseType res2 = HexToBin(str2);
	BaseType res = "";
	/*BaseType res_max;
	if (res1.size() >= res2.size())
	{
		res_max = res1;
	}
	else
	{
		res_max = res2;
	}*/
	for (int i = 0; i < res1.size(); i++)
	{
		if (res1[i] == res2[i])
		{
			res += "0";
		}
		else
		{
			res += "1";
		}
	}
	return BinToHex(res);
}
BaseType LeftShift(BaseType str, int len)//实现左移函数
{
	BaseType res = HexToBin(str);
	res = res.substr(len) + res.substr(0, len);//substr( pos,len)从初始位置 pos开始读取长度为len个字符,这里前面len是指pos的意思，而len为空，即从len位置开始读取后面的所有字符
	return BinToHex(res);
}

BaseType yi(BaseType str)//乙函数,非线性变换
{
	BaseType Sbox[16][16]={{"D6","90","E9","FE","CC","E1","3D","B7","16","B6","14","C2","28","FB","2C","05"},
		{ "2B","67","9A","76","2A","BE","04","C3","AA","44","13","26","49","86","06","99" },
		{ "9C","42","50","F4","91","EF","98","7A","33","54","0B","43","ED","CF","AC","62" },
		{ "E4","B3","1C","A9","C9","08","E8","95","80","DF","94","FA","75","8F","3F","A6" },
		{ "47","07","A7","FC","F3","73","17","BA","83","59","3C","19","E6","85","4F","A8" },
		{ "68","6B","81","B2","71","64","DA","8B","F8","EB","0F","4B","70","56","9D","35" },
		{ "1E","24","0E","5E","63","58","D1","A2","25","22","7C","3B","01","21","78","87" },
		{ "D4","00","46","57","9F","D3","27","52","4C","36","02","E7","A0","C4","C8","9E" },
		{ "EA","BF","8A","D2","40","C7","38","B5","A3","F7","F2","CE","F9","61","15","A1" },
		{ "E0","AE","5D","A4","9B","34","1A","55","AD","93","32","30","F5","8C","B1","E3" },
		{ "1D","F6","E2","2E","82","66","CA","60","C0","29","23","AB","0D","53","4E","6F" },
		{ "D5","DB","37","45","DE","FD","8E","2F","03","FF","6A","72","6D","6C","5B","51" },
		{ "8D","1B","AF","92","BB","DD","BC","7F","11","D9","5C","41","1F","10","5A","D8" },
		{ "0A","C1","31","88","A5","CD","7B","BD","2D","74","D0","12","B8","E5","B4","B0" },
		{ "89","69","97","4A","0C","96","77","7E","65","B9","F1","09","C5","6E","C6","84" },
		{ "18","F0","7D","EC","3A","DC","4D","20","79","EE","5F","3E","D7","CB","39","48" } };
	BaseType res = "";
	for (int i = 0; i < 4; i++)
	{
		res += Sbox[HexToDec(str[2 * i])][HexToDec(str[2 * i + 1])];//密钥一共为128位，分成了四份K0,K1,K2,K3然后和CK0异或，所以一共是32位，32位分成四个8bit再经过S盒，8bit中的前4bit看作16进制，后4bit也看做16进制。所以输入的str一共是32bit的。假设输入字符CA，然后先通过HexToDec函数转化CA为12和10，所对应的十进制，注意此时我们默认这个CA是为16进制的。
	}
	return res;
}
BaseType L1(BaseType str)//L1函数,线性变换函数,这里的L1函数是在轮函数时的L函数
{
	return XOR(XOR(XOR(XOR(str, LeftShift(str, 2)), LeftShift(str, 10)), LeftShift(str, 18)), LeftShift(str, 24));
}
BaseType L2(BaseType str)//L2函数，这里的L2是生成轮密钥时的L函数
{
	return XOR(XOR(str, LeftShift(str, 13)), LeftShift(str,23));
}
BaseType T1(BaseType str)//L1所对应的T函数
{
	return L1(yi(str));
}
BaseType T2(BaseType str)//L2所对应的T函数
{
	return L2(yi(str));
}
//轮密钥拓展实现
BaseType KeyExtend(BaseType MK)//加密密钥MK=(MK0,MK1,MK2,MK3)
{
	BaseType FK[4] = { "A3B1BAC6","56AA3350","677D9197", "B27022DC" };//系统参数FK=(FK0,FK1,FK2,FK3)
	BaseType CK[32] = { "00070E15","1C232A31","383F464D","545B6269",
					"70777E85","8C939AA1","A8AFB6BD","C4CBD2D9",
					"E0E7EEF5","FC030A11","181F262D","343B4249",
					"50575E65","6C737A81","888F969D","A4ABB2B9",
					"C0C7CED5","DCE3EAF1","F8FF060D","141B2229",
					"30373E45","4C535A61","686F767D","848B9299",
					"A0A7AEB5","BCC3CAD1","D8DFE6ED","F4FB0209",
					"10171E25","2C333A41","484F565D","646B7279" };//固定参数CK=(CK0,CK1...CK31)
	BaseType K[36] = { XOR(MK.substr(0,8),FK[0]),XOR(MK.substr(8,8),FK[1]),XOR(MK.substr(16,8),FK[2]),XOR(MK.substr(24,8),FK[3]) };//子密钥,这里一共有36个字符串，每8个字符为一个字符串
	BaseType rk_i = "";
	for (int i = 0; i < 32; i++)//i=0,1,2...31
	{
		K[i + 4] = XOR(K[i], T2(XOR(XOR(XOR(XOR(K[i], K[i + 1]), K[i + 2]), K[i + 3]), CK[i])));
		rk_i+= K[i + 4];//rk_i从0到31，一共有32个字符串，每个字符串8个字符
	}
	return rk_i;
}
BaseType SM4EnCry(BaseType plaintext, BaseType key)//SM4加密实现//key是MK
{
	// HLS接口综合，具体用法在ug902中，也可参考 https://blog.csdn.net/weixin_40162095/article/details/114758125
	//#pragma HLS INTERFACE m_axi depth=8 port=V_Out offset=slave // vitis hls会自动进行接口综合，vivado hls需要手动
	//#pragma HLS INTERFACE m_axi depth=8 port=V_In offset=slave // 一般将数组元素定义为m_axi接口，depth为数组长度；一般将变量元素定义为s_axilite接口
	//#pragma HLS INTERFACE m_axi depth=64 port=M offset=slave  // 一般都设为offset=slave,这样方便自己显式的指明地址
	//#pragma HLS INTERFACE s_axilite port=return // 对模块的启动方式进行约束。

	//cout << "开始:" << endl;
	BaseType X[36] = { plaintext.substr(0,8),plaintext.substr(8,8),plaintext.substr(16,8),plaintext.substr(24,8) };//明文就是加密的密钥，K0,K1,K2,K3,明文至少要有32个字符,每8个字符组成一个字符串
	BaseType rk = KeyExtend(key);//拓展密钥完成，这里的拓展密钥后为32个字符串，每个字符串8个字符
	for (int i = 0; i < 32; i++)
	{
		X[i + 4] = XOR(X[i], T1(XOR(XOR(XOR(X[i + 1], X[i + 2]), X[i + 3]), rk.substr(i*8,8))));//因为i=0,1...31,所以X[i+4]=X[35]最多，所以一共有36个明文，从X[0]到X[35],8个字符为一个字符串，所以rk[0]为前8个字符
		//cout << "rk[" + to_string(i) + "] = " + rk.substr(i * 8, 8) + " "<< endl;
		//cout << "X["+to_string(i+4)+"] = "<<X[i + 4]<< endl;
	}
	//cout << "最后一步反序变换" << endl;
	return X[35] + X[34] + X[33] + X[32];
}
//解密，轮密钥使用顺序相反
BaseType SM4DeCry(BaseType ciphertext, BaseType key)
{
	// HLS接口综合，具体用法在ug902中，也可参考 https://blog.csdn.net/weixin_40162095/article/details/114758125
	//#pragma HLS INTERFACE m_axi depth=8 port=V_Out offset=slave // vitis hls会自动进行接口综合，vivado hls需要手动
	//#pragma HLS INTERFACE m_axi depth=8 port=V_In offset=slave // 一般将数组元素定义为m_axi接口，depth为数组长度；一般将变量元素定义为s_axilite接口
	//#pragma HLS INTERFACE m_axi depth=64 port=M offset=slave  // 一般都设为offset=slave,这样方便自己显式的指明地址
	//#pragma HLS INTERFACE s_axilite port=return // 对模块的启动方式进行约束。

	//cout << "开始:" << endl;
	BaseType P[36] = { ciphertext.substr(0,8),ciphertext.substr(8,8),ciphertext.substr(16,8),ciphertext.substr(24,8) };//明文就是加密的密钥，K0,K1,K2,K3,明文至少要有32个字符,每8个字符组成一个字符串
	BaseType rk = KeyExtend(key);//拓展密钥完成，这里的拓展密钥后为32个字符串，每个字符串8个字符
	for (int i = 0; i < 32; i++)
	{
		P[i + 4] = XOR(P[i], T1(XOR(XOR(XOR(P[i + 1], P[i + 2]), P[i + 3]), rk.substr((31-i) * 8, 8))));//因为i=0,1...31,所以X[i+4]=X[35]最多，所以一共有36个明文，从X[0]到X[35],8个字符为一个字符串，所以rk[0]为前8个字符
		//cout << "rk[" + to_string(i) + "] = " + rk.substr(8*(31-i), 8) + " " << endl;
		//cout << "P[" + to_string(i+4) + "] = " << P[i + 4] << endl;
	}
	//cout << "最后一步反序变换" << endl;
	return P[35] + P[34] + P[33] + P[32];
}
