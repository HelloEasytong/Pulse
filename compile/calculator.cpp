#include <iostream>
#include <string>
#include <cmath>
#include <cstdlib>
#include <sstream>
#include <type_traits>

using namespace std;

// 判断字符串是否为整数
bool isInteger(const string& s) {
    if (s.empty()) return false;
    size_t pos = 0;
    if (s[pos] == '-') pos++; // 处理负数
    for (; pos < s.length(); pos++) {
        if (!isdigit(s[pos])) return false;
    }
    return true;
}

// 主函数
int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " operation num1 num2\n"
             << "Operations: add, sub, mul, div, pow" << endl;
        return 1;
    }

    string operation = argv[1];
    string num1_str = argv[2];
    string num2_str = argv[3];

    // 判断输入是否为整数
    bool use_long_long = isInteger(num1_str) && isInteger(num2_str);

    if (use_long_long) {
        // 使用 long long 类型
        long long num1, num2;
        try {
            num1 = stoll(num1_str);
            num2 = stoll(num2_str);
        } catch (...) {
            cerr << "Error: Invalid integer format" << endl;
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
            cout << static_cast<long long>(pow(num1, num2));
        } else {
            cerr << "Error: Invalid operation. Valid options: add, sub, mul, div, pow" << endl;
            return 1;
        }
    } else {
        // 使用 double 类型
        double num1, num2;
        try {
            num1 = stod(num1_str);
            num2 = stod(num2_str);
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
    }

    return 0;
}