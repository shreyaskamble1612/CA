#include<bits/stdc++.h>

using namespace std;

int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }
    return climbStairs(n - 1) + climbStairs(n - 2);;
}

int main() {
    int n = 45;
    cout << climbStairs(n) << endl; 
    return 0;
}