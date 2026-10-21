#include<bits/stdc++.h>
using namespace std;

string new_string(vector<string> n_strings){
  string s = "";
  int n = n_strings.size();
  for(int i = 0;i < n; i ++) 
    if(n_strings[i][i] == '0') s += '1';
    else s += '0';
  return s;
  
}
