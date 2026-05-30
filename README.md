# 🧮 Windows 计算器 (Calculator)

一个完整的计算器项目，包含 **命令行版 (C++)** 和 **GUI 版 (Python)** 两种实现，GUI 版完美模仿 Windows 11 标准计算器的外观与交互体验。

---

## 📸 项目预览

### GUI 版 — Windows 11 风格
- 暗色主题，与 Windows 11 原生计算器一致的配色方案
- 双行显示（历史表达式 + 当前输入）
- 支持三种模式：**标准** / **科学** / **程序员**
- 完整的记忆功能（MC / MR / M+ / M- / MS）
- 键盘完全映射，支持快捷键操作

### CLI 版 — 命令行交互
- 美观的命令行界面（UTF-8 字符框线）
- 智能错误提示，精确指出输入问题
- 支持特殊命令：`help`、`clear`、`quit`
- 自动去除尾部多余零，输出美观

---

## 🚀 快速开始

### GUI 版（推荐）

**要求：** Python 3.7+（自带 tkinter）

```bash
python calculator_gui.py
```

无需安装任何第三方依赖，Python 标准库即可运行。

### CLI 版

**要求：** g++（MinGW / MSVC 均可）

```bash
# 编译
g++ calculator.cpp -o calculator.exe

# 运行
./calculator.exe
```

---

## 📦 下载

Windows 用户可直接下载编译好的可执行文件：

- **[calculator.zip](https://github.com/programlj/calculator/raw/main/calculator.zip)** (27 KB)
  - 解压后运行 `calculator.exe` 即可使用命令行版计算器
  - 无需安装任何依赖，开箱即用

---

## ⌨️ 功能特性

### 标准模式

| 功能 | 说明 |
|------|------|
| `+` `-` `x` `/` | 四则运算 |
| `%` | 百分比（除以 100） |
| `1/x` | 倒数 |
| `x^2` | 平方 |
| `sqrt(x)` | 平方根 |
| `+/-` | 正负号切换 |
| `C` | 全部清除 |
| `CE` | 清除当前输入 |
| `Backspace` | 退格 |

### 记忆功能

| 按钮 | 功能 |
|------|------|
| `MC` | 清除记忆 |
| `MR` | 调用记忆 |
| `M+` | 当前值加到记忆 |
| `M-` | 从记忆减去当前值 |
| `MS` | 存储到记忆 |

### 科学模式

| 功能 | 说明 |
|------|------|
| `sin` `cos` `tan` | 三角函数（支持 DEG/RAD） |
| `log` `ln` | 常用对数 / 自然对数 |
| `10^x` `e^x` | 指数函数 |
| `n!` | 阶乘 |
| `x^y` | 幂运算 |
| `y sqrt(x)` | 开任意次方 |
| `pi` `e` | 数学常数 |
| `(` `)` | 括号优先级 |

### 程序员模式

| 功能 | 说明 |
|------|------|
| `AND` `OR` `XOR` `NOT` | 按位逻辑运算 |
| `LSH` `RSH` | 左右移位 |
| `HEX` `DEC` `OCT` `BIN` | 四种进制切换 |
| `A`-`F` | 十六进制数字 |

---

## 🎨 设计细节

- **颜色方案：** 背景 `#202020`，数字 `#333333`，运算符 `#FF9500`，功能 `#505050`
- **字体：** Segoe UI，与 Windows 11 系统一致
- **悬停效果：** 所有按钮支持 hover 变色
- **自适应窗口：** 标准 340x600，科学 430x680，程序员 430x760
- **错误状态：** 红色文字提示，任何按键自动清除错误
- **重复等号：** 按 `=` 后继续按 `=` 可重复上次运算

---

## 📁 项目结构

```
calculator/
├── calculator.cpp         # C++ 命令行版计算器
├── calculator_gui.py      # Python GUI 版计算器 (Windows 11 风格)
├── .gitignore             # Git 忽略规则
└── README.md              # 项目说明（本文件）
```

---

## 🔧 编译说明

### C++ 命令行版

| 平台 | 编译命令 |
|------|----------|
| Windows (MinGW) | `g++ calculator.cpp -o calculator.exe` |
| Windows (MSVC) | `cl calculator.cpp` |
| Linux / macOS | `g++ calculator.cpp -o calculator` |

> Windows 下编译时会自动设置控制台编码为 UTF-8，正确显示中文提示。

### Python GUI 版

- **依赖：** 无（仅使用 Python 标准库 `tkinter` + `math`）
- **兼容：** Windows / Linux / macOS，只要 Python 带 tkinter 即可

---

## 📝 使用示例

### CLI 版

```
  [1] 请输入算式 > 3 + 5
  ---
  OK 3 + 5 = 8
  ---

  [2] 请输入算式 > 10.5 * 2.3
  ---
  OK 10.5 * 2.3 = 24.15
  ---

  [3] 请输入算式 > quit
  感谢使用，再见！
```

### GUI 版

直接运行 `python calculator_gui.py`，使用鼠标点击按钮或键盘输入即可。

---

## 📄 License

MIT License
