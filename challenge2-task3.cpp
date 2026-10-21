#include<bits/stdc++.h>
using namespace std;
int smallestNonOccuringInt(vector<int> nums){
  set<int> sorted_nums;
  for(auto k: nums) 
    if(k > 0) sorted_nums.insert(k);
  int i = 0;
  for(; i < sorted_nums.size(); i++)
    if(*next(sorted_nums.begin(), i) > i+1) return i+1;
  return i+1;
}
