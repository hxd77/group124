#include <iostream>
#include "merkle tree.h"
#include "sha256.h"
using namespace std;
#define MAX 100000;
int tree::verify(string hash)
{
	node* temp = nullptr;
	string act_hash = hash;

	for (int i = 0; i < base[0].size(); i++)
	{
		if (base[0][i]->getHash() == hash)
		{
			temp = base[0][i];
		}
	}
	if (temp == nullptr)
	{
		return 0;
	}
	do
	{
		if (temp->checkDir() == 0)
		{
			act_hash = sha2::hash256_hex_string(act_hash + temp->change()->getHash());
		}
		else
		{
			act_hash = sha2::hash256_hex_string(temp->change()->getHash() + act_hash);
		}

		temp = temp->parent;
	} while ((temp->parent) != NULL); 
	if (act_hash == root) {
		cout << "存在验证的数据";
		return 1;
	};
	if (act_hash != root){
		cout << "不存在验证的数据";
		return 0;
};
}
int main()
{
	string test = std::to_string(6666);
	vector<string> v;

	for (int i = 0; i < 10000; i++) {
		v.push_back(std::to_string(i));
	}
	
	tree ntree;
	ntree.buildBaseLeafes(v);
	ntree.buildTree();

	test = sha2::hash256_hex_string(test);

	cout << "想验证的数据的哈希值: " << test << endl;

	ntree.verify(test);
}
