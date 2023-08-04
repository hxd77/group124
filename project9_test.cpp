#include"sm4.h"
using namespace std;
int main()
{
	//分组长度128bit，密钥长度128bit
	BaseType str="0123456789ABCDEF8976543210ABCFDE";
	cout << "明文:" << str.substr(0, 8)<<" "<< str.substr(8, 8)<<" " << str.substr(16, 8)<< " " << str.substr(24, 8) << endl;
	BaseType key = "0987654321ABCDEFFEDCBA9876543210";
	cout << "密钥:" << key.substr(0, 8) << " " << key.substr(8, 8) << " " << key.substr(16, 8) << " " << key.substr(24, 8) << endl;
	BaseType cipher = SM4EnCry(str, key);
	cout << "密文:" << cipher.substr(0, 8) << " " << cipher.substr(8, 8) << " " << cipher.substr(16, 8) << " " << cipher.substr(24, 8) << endl;
	cout << "解密密钥:" << key.substr(0, 8) << " " << key.substr(8, 8) << " " << key.substr(16, 8) << " " << key.substr(24, 8) << endl;
	BaseType plain = SM4DeCry(cipher, key);
	cout << "解密明文:" << plain.substr(0, 8) << " " << plain.substr(8, 8) << " " << plain.substr(16, 8) << " " << plain.substr(24, 8) << endl;
	return 0;
}