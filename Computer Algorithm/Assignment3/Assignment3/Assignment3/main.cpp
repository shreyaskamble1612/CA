#include <iostream>
#include <omp.h>
#include <vector>
#include <map>

using namespace std;
#define N 1024

void matrixMultiply(vector<vector<double>>& A, 
                    vector<vector<double>>& B, 
                    vector<vector<double>>& C, 
                    int num_threads) {
    // #pragma omp parallel for num_threads(num_threads)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main() {
    vector<vector<double>> A(N, vector<double>(N));
    vector<vector<double>> B(N, vector<double>(N));
    vector<vector<double>> C(N, vector<double>(N));
    
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            A[i][j] = (i + j);
            B[i][j] = abs(i - j + 1);
        }
    }

    map<int, double> results;

    int num_runs = 10;
    for (int threads = 1; threads <= 8; threads++) {
        double total_time = 0.0;
        for (int run = 0; run < num_runs; run++) {
            double start_time = omp_get_wtime();
            matrixMultiply(A, B, C, threads);
            double end_time = omp_get_wtime();
            total_time += (end_time - start_time);
        }
        double avg_time = total_time / num_runs;
        results[threads] = avg_time;
    }

    // Print results in a formatted table
    cout << "Threads | Average Time (seconds)" << endl;
    cout << "------------------------------" << endl;
    for(auto &it: results) {
        cout << it.first << " | " << it.second << endl;
    }

    return 0;
}
