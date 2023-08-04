#pragma once
#include <iostream>
#pragma once
#include <iostream>
#include <sstream>
#include "sha256.h"
#include <string>
#include <vector>
using namespace std;

class node
{
public:
	string hash;
	node* parent;
	node* left;
	node* right;
	node();
	string getHash();
	int checkDir();
	node* change();
	void setHash(string hash);
	virtual ~node();
};
node::node()
{
	parent = nullptr;
	left = nullptr;
	right = nullptr;
}

//设置哈希值
void node::setHash(string hash)
{
	this->hash = sha2::hash256_hex_string(hash);
}

node* node::change() 
{
	node* aparent = parent;

	if (aparent->left == this) return aparent->right;
	else return aparent->left;
}

string node::getHash()
{
	return hash;
}
int node::checkDir()
{
	if (parent->left == this) return 0;
	else return 1;
}

node::~node() {}

#pragma once

using namespace std;
class tree
{
private:
	string root;
	int level;
	int doublE(vector<node*>& node_vector);
	vector<vector<node*>> base; 
public:
	tree();
	void buildTree();
	void buildBaseLeafes(vector<string> base_leafs);
	int verify(string hash);
	virtual ~tree();
};

tree::tree() {}

int tree::doublE(vector<node*>& node) 
{
	int vectSize = node.size();
	if ((vectSize % 2) != 0) 
	{
		node.push_back(node.end()[-1]);
		vectSize++;
	}
	return vectSize;
}

void tree::buildTree() 
{
	level = 0;
	do
	{
		level++;
		vector<node*> nodes;
		doublE(base.end()[-1]); 

		for (int i = 0; i < base.end()[-1].size(); i += 2)
		{
			node* temp = new node; 
			base.end()[-1][i]->parent=temp;
			base.end()[-1][i + 1]->parent=temp;
			temp->hash= sha2::hash256_hex_string(base.end()[-1][i]->hash + base.end()[-1][i + 1]->hash);
			temp->left = base.end()[-1][i];
			temp->right=base.end()[-1][i + 1];
			nodes.push_back(temp);
		}

		base.push_back(nodes); 

		cout<<"第"<<level << "层的结点有 " << base.end()[-1].size() << " 个:" << endl;
	} while (base.end()[-1].size() > 1); //

	root = base.end()[-1][0]->getHash(); 

	cout << "最终的根节点为 : " << root << endl << endl;
}

void tree::buildBaseLeafes(vector<string> leafs) 
{
	vector<node*> nodes;


	for (auto leaf : leafs) 
	{
		node* new_node = new node;
		new_node->hash= sha2::hash256_hex_string(leaf);
		nodes.push_back(new_node);
	}

	base.push_back(nodes);
	cout << endl;
}

tree::~tree() {}
#pragma once
