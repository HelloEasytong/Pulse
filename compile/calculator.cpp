#include <iostream>
#include <string>
#include <cmath>
#include <cstdlib>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " operation num1 num2\n"
             << "Operations: add, sub, mul, div, pow" << endl;
        return 1;
    }
    
    string operation = argv[1];
    double num1, num2;
    
    try {
        num1 = stod(argv[2]);
        num2 = stod(argv[3]);
    } catch (...) {
        cerr << "Error: Invalid number format" << endl;
        return 1;
    }
    
    if (operation == "add") {
        cout << num1 + num2;
    } else if (operation == "sub") {
        cout << num1 - num2;
    } else if (operation == "mul") {
        cout << num1 * num2;
    } else if (operation == "div") {
        if (num2 == 0) {
            cerr << "Error: Division by zero" << endl;
            return 1;
        }
        cout << num1 / num2;
    } else if (operation == "pow") {
        cout << pow(num1, num2);
    } else {
        cerr << "Error: Invalid operation. Valid options: add, sub, mul, div, pow" << endl;
        return 1;
    }
    
    return 0;
}