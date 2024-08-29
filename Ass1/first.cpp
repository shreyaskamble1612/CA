#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;

vector<int> generateRandomNumbers(int size, int min, int max) {
    vector<int> numbers(size);
    for (int i = 0; i < size; ++i) {
        numbers[i] = rand() % (max - min + 1) + min;
    }
    return numbers;
}

bool isOdd(int number) {
    return number % 2 != 0;
}

bool isEven(int number) {
    return number % 2 == 0;
}

bool isPrime(int number) {
    if (number <= 1) return false;
    for (int i = 2; i <= sqrt(number); ++i) {
        if (number % i == 0) return false;
    }
    return true;
}

double factorial(int number) {
    if (number == 0) return 1;
    double fact = 1;
    for (double i = 1; i <= number; ++i) {
        fact *= i;
    }
    return fact;
}

vector<int> computePrefixSum(const vector<int>& numbers) {
    vector<int> prefixSum(numbers.size());
    prefixSum[0] = numbers[0];
    for (int i = 1; i < numbers.size(); ++i) {
        prefixSum[i] = prefixSum[i - 1] + numbers[i];
    }
    return prefixSum;
}

double computeAverage(const vector<int>& numbers) {
    int sum = 0;
    for (int i = 0; i < numbers.size(); ++i) {
        sum += numbers[i];
    }
    return static_cast<double>(sum) / numbers.size();
}

int main() {
    srand(time(0));
    vector<int> numbers = generateRandomNumbers(100, 1, 10000);
    for (int i = 0; i < numbers.size(); ++i) {
        cout << "Number: " << numbers[i] << " | ";
        cout << (isOdd(numbers[i]) ? "Odd" : "Even") << " | ";
        cout << (isPrime(numbers[i]) ? "Prime" : "Not Prime") << " | ";
        cout << "Factorial: " << factorial(numbers[i]) << endl;
    }
    vector<int> prefixSum = computePrefixSum(numbers);
    double average = computeAverage(numbers);
    cout << "Prefix Sum: ";
    for (int i = 0; i < prefixSum.size(); ++i) {
        cout << prefixSum[i] << " ";
    }
    cout << endl;
    cout << "Average: " << average << endl;
    return 0;
}
