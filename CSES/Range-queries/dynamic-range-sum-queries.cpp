#include<bits/stdc++.h>
#include<iostream>

using namespace std;

vector<long long> dp, v;

void build(int at, int l, int r){
    if(l==r){
        dp[at]==v[l];
        return;
    }
    int mid = (l+r)/2;
    build(2*at+1, l, mid);
    build(2*at+2, mid+1, r);
    dp[at] = dp[2*at+1] + dp[2*at + 2];

}

int main(){
    int n,q;
    cin>>n>>q;
   
    dp.assign(4*n, 0);
    v.assign(n, 0);

    for(int i=0; i<n; i++){
        cin>>v[i];
    }

    
    build(0, 0, n-1);
    

}
