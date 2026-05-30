/**
 * Windows 命令行计算器 (Command-line Calculator)
 * 支持加减乘除四则运算、小数计算、完善的错误处理
 * 编译: g++ calculator.cpp -o calculator.exe
 * 运行: calculator.exe
 */

#include <iostream>
#include <string>
#include <sstream>
#include <limits>
#include <iomanip>
#include <cctype>
#include <cstdlib>

// ============================================================
// 工具函数
// ============================================================

/// 去除字符串首尾空白字符（空格、制表符、回车换行）
std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r\v\f");
    if (first == std::string::npos) return "";
    size_t last = str.find_last_not_of(" \t\n\r\v\f");
    return str.substr(first, last - first + 1);
}

/// 将字符串转为小写（用于命令判断）
std::string toLower(const std::string& str) {
    std::string result = str;
    for (char& c : result) {
        if (c >= 'A' && c <= 'Z') c += ('a' - 'A');
    }
    return result;
}

/// 判断字符串是否为有效的数字（支持整数和小数，包括负数）
bool isValidNumber(const std::string& s) {
    if (s.empty()) return false;
    std::istringstream iss(s);
    double d;
    iss >> std::noskipws >> d;
    return iss.eof() && !iss.fail();
}

// ============================================================
// 显示函数
// ============================================================

void showWelcome() {
    std::cout << "\n";
    std::cout << "  ╔══════════════════════════════════════════╗\n";
    std::cout << "  ║     命 令 行 计 算 器  v1.0             ║\n";
    std::cout << "  ║     Command-line Calculator               ║\n";
    std::cout << "  ╚══════════════════════════════════════════╝\n";
}

void showHelp() {
    std::cout << "\n";
    std::cout << "  ┌────────── 使 用 说 明 ──────────┐\n";
    std::cout << "  │                                    │\n";
    std::cout << "  │  输入格式: <数字> <运算符> <数字>  │\n";
    std::cout << "  │  示例: 3 + 5                       │\n";
    std::cout << "  │        10.5 * 2.3                  │\n";
    std::cout << "  │        -8 / 4                      │\n";
    std::cout << "  │                                    │\n";
    std::cout << "  │  支持的运算符:                      │\n";
    std::cout << "  │    +  加法 (Addition)               │\n";
    std::cout << "  │    -  减法 (Subtraction)            │\n";
    std::cout << "  │    *  乘法 (Multiplication)         │\n";
    std::cout << "  │    /  除法 (Division)               │\n";
    std::cout << "  │                                    │\n";
    std::cout << "  │  特殊命令:                          │\n";
    std::cout << "  │    help / 帮助    显示本帮助        │\n";
    std::cout << "  │    clear / cls    清屏              │\n";
    std::cout << "  │    quit / exit    退出程序          │\n";
    std::cout << "  │                                    │\n";
    std::cout << "  │  可直接输入 q 或按 Ctrl+C 退出      │\n";
    std::cout << "  └────────────────────────────────────┘\n";
}

void showDivider() {
    std::cout << "  ─────────────────────────────────────\n";
}

// ============================================================
// 核心：表达式解析
// ============================================================

/**
 * 解析用户输入的表达式
 * 支持格式: <数字> <运算符> <数字>  (空格可选)
 *
 * @param expr   用户输入的原始字符串
 * @param a      解析出的第一个操作数（输出）
 * @param op     解析出的运算符（输出）
 * @param b      解析出的第二个操作数（输出）
 * @param error  错误信息（输出，成功时为空）
 * @return       解析成功返回 true，失败返回 false
 */
bool parseExpression(const std::string& expr, double& a, char& op, double& b, std::string& error) {
    std::istringstream iss(expr);

    // 1. 尝试读取第一个数字
    if (!(iss >> a)) {
        error = "无法解析第一个操作数，请确认输入的是有效数字。";
        return false;
    }

    // 2. 跳过空白，读取运算符
    char peekChar;
    // 跳过运算符前的空白
    while (iss.peek() != EOF && std::isspace(static_cast<unsigned char>(iss.peek()))) {
        iss.get();
    }

    if (iss.peek() == EOF) {
        error = "缺少运算符和第二个操作数。\n        正确格式: <数字> <运算符> <数字>，例如 3 + 5";
        return false;
    }

    iss.get(op);

    // 验证运算符合法性
    if (op != '+' && op != '-' && op != '*' && op != '/') {
        error = std::string("不支持的运算符 '") + op + "'。\n        支持的运算符: + (加)  - (减)  * (乘)  / (除)";
        return false;
    }

    // 3. 跳过空白，读取第二个数字
    while (iss.peek() != EOF && std::isspace(static_cast<unsigned char>(iss.peek()))) {
        iss.get();
    }

    if (iss.peek() == EOF) {
        error = "缺少第二个操作数。\n        正确格式: <数字> <运算符> <数字>，例如 3 + 5";
        return false;
    }

    if (!(iss >> b)) {
        error = "无法解析第二个操作数，请确认输入的是有效数字。";
        return false;
    }

    // 4. 检查是否有多余内容（只允许尾部空白）
    std::string remaining;
    std::getline(iss, remaining);
    remaining = trim(remaining);
    if (!remaining.empty()) {
        error = "表达式包含多余内容: \"" + remaining + "\"\n        请只输入 <数字> <运算符> <数字> 的格式。";
        return false;
    }

    // 解析成功
    error = "";
    return true;
}

// ============================================================
// 核心：执行计算
// ============================================================

/**
 * 执行四则运算
 *
 * @param a      第一个操作数
 * @param op     运算符
 * @param b      第二个操作数
 * @param result 计算结果（输出）
 * @param error  错误信息（输出，成功时为空）
 * @return       计算成功返回 true，失败返回 false
 */
bool compute(double a, char op, double b, double& result, std::string& error) {
    switch (op) {
        case '+':
            result = a + b;
            error = "";
            return true;

        case '-':
            result = a - b;
            error = "";
            return true;

        case '*':
            result = a * b;
            error = "";
            return true;

        case '/':
            // 检查除数为零
            if (b == 0.0) {
                error = "数学错误：除数不能为零！在实数范围内，除以零是未定义的操作。";
                return false;
            }
            result = a / b;
            error = "";
            return true;

        default:
            error = std::string("内部错误：未知运算符 '") + op + "'。";
            return false;
    }
}

// ============================================================
// 格式化输出
// ============================================================

/// 智能格式化输出：输出完整精度后去掉尾部多余零
std::string formatNumber(double num) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(12) << num;
    std::string s = oss.str();

    // 去掉末尾多余的零
    size_t dotPos = s.find('.');
    if (dotPos != std::string::npos) {
        size_t lastNonZero = s.find_last_not_of('0');
        if (lastNonZero > dotPos) {
            s = s.substr(0, lastNonZero + 1);
        } else if (lastNonZero == dotPos) {
            // 小数部分全为零，去掉小数点
            s = s.substr(0, dotPos);
        }
    }
    return s;
}

// ============================================================
// 主函数
// ============================================================

int main() {
    // 设置控制台输出编码为 UTF-8（Windows 兼容）
    #ifdef _WIN32
        std::system("chcp 65001 > nul 2>&1");
    #endif

    showWelcome();
    showHelp();

    std::string input;
    int count = 0;  // 已执行的计算次数

    while (true) {
        // 显示提示符
        std::cout << "\n  [" << (count + 1) << "] 请输入算式 > ";
        std::getline(std::cin, input);

        // 处理 EOF（Ctrl+Z）
        if (std::cin.eof()) {
            std::cin.clear();
            std::cout << "\n\n  已检测到 EOF，正在退出...\n";
            break;
        }

        // 空白输入，跳过
        std::string trimmed = trim(input);
        if (trimmed.empty()) {
            continue;
        }

        // 检查是否为特殊命令
        std::string cmd = toLower(trimmed);

        if (cmd == "quit" || cmd == "exit" || cmd == "q") {
            std::cout << "\n  感谢使用，再见！\n\n";
            break;
        }

        if (cmd == "help" || cmd == "帮助" || cmd == "?") {
            showHelp();
            continue;
        }

        if (cmd == "clear" || cmd == "cls") {
            #ifdef _WIN32
                std::system("cls");
            #else
                std::system("clear");
            #endif
            showWelcome();
            continue;
        }

        // 尝试解析表达式
        double a, b, result;
        char op;
        std::string parseError;

        if (!parseExpression(trimmed, a, op, b, parseError)) {
            std::cout << "\n  ✗ 输入格式错误：\n    " << parseError << "\n";
            std::cout << "  (输入 help 可查看帮助)\n";
            continue;
        }

        // 执行计算
        std::string calcError;
        if (!compute(a, op, b, result, calcError)) {
            std::cout << "\n  ✗ 计算错误：\n    " << calcError << "\n";
            continue;
        }

        // 显示结果
        std::string aStr = formatNumber(a);
        std::string bStr = formatNumber(b);
        std::string rStr = formatNumber(result);

        showDivider();
        std::cout << "  ✓ " << aStr << " " << op << " " << bStr << " = " << rStr << "\n";
        showDivider();

        count++;
    }

    return 0;
}
