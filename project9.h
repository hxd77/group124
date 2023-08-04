#pragma once
#include<iostream>
using namespace std;
typedef string BaseType;
BaseType SM4EnCry(BaseType plaintext, BaseType key);
BaseType SM4DeCry(BaseType ciphertext, BaseType key);

