#!/usr/bin/env python3
"""
Windows 11 风格命令行计算器 (GUI版)
使用 Python tkinter，完全模仿 Windows 11 标准计算器外观与交互
运行: python calculator_gui.py
"""

import tkinter as tk
from tkinter import font as tkfont
import math


class CalculatorApp:
    """Windows 11 风格计算器应用"""

    # ── 颜色常量 ──────────────────────────────────────────
    BG_DARK    = "#202020"   # 窗口背景
    NUM_BG     = "#333333"   # 数字按钮背景
    NUM_HOVER  = "#555555"   # 数字按钮悬停
    OP_BG      = "#FF9500"   # 运算符按钮背景
    OP_HOVER   = "#FFB340"   # 运算符按钮悬停
    FUNC_BG    = "#505050"   # 功能按钮背景
    FUNC_HOVER = "#707070"   # 功能按钮悬停
    FG_WHITE   = "#FFFFFF"   # 白色文字
    HIST_FG    = "#888888"   # 历史行灰色
    ERR_FG     = "#FF4444"   # 错误文字红色

    # ── 按钮布局（每行4个） ────────────────────────────────
    # 格式：(文本, 行, 列, 类型)
    # 类型: 'func' | 'operator' | 'number' | 'equals'
    BUTTONS = [
        # Row 0
        ("%",     0, 0, "func"),
        ("CE",    0, 1, "func"),
        ("C",     0, 2, "func"),
        ("←",     0, 3, "func"),
        # Row 1
        ("1/x",   1, 0, "func"),
        ("x²",    1, 1, "func"),
        ("√x",    1, 2, "func"),
        ("÷",     1, 3, "operator"),
        # Row 2
        ("7",     2, 0, "number"),
        ("8",     2, 1, "number"),
        ("9",     2, 2, "number"),
        ("×",     2, 3, "operator"),
        # Row 3
        ("4",     3, 0, "number"),
        ("5",     3, 1, "number"),
        ("6",     3, 2, "number"),
        ("−",     3, 3, "operator"),
        # Row 4
        ("1",     4, 0, "number"),
        ("2",     4, 1, "number"),
        ("3",     4, 2, "number"),
        ("+",     4, 3, "operator"),
        # Row 5
        ("±",     5, 0, "func"),
        ("0",     5, 1, "number"),
        (".",     5, 2, "number"),
        ("=",     5, 3, "equals"),
    ]


    # ---- 科学模式按钮布局（5列x8行） --------------------------
    BUTTONS_SCIENTIFIC = [
        # Row 0: 括号 & 清除
        ("(",    0, 0, "paren"),  (")",    0, 1, "paren"),
        ("CE",   0, 2, "func"),   ("C",    0, 3, "func"),
        ("←",    0, 4, "func"),
        # Row 1: 三角函数 & 对数
        ("sin",  1, 0, "sci_func"), ("cos",  1, 1, "sci_func"),
        ("tan",  1, 2, "sci_func"), ("log",  1, 3, "sci_func"),
        ("ln",   1, 4, "sci_func"),
        # Row 2: 幂函数
        ("x²",   2, 0, "func"),   ("√x",   2, 1, "func"),
        ("x^y",  2, 2, "sci_func"), ("10^x", 2, 3, "sci_func"),
        ("e^x",  2, 4, "sci_func"),
        # Row 3: 倒数 & 阶乘 & 常数 & 开方
        ("1/x",  3, 0, "func"),   ("n!",   3, 1, "sci_func"),
        ("π",    3, 2, "sci_func"), ("e",    3, 3, "sci_func"),
        ("y√x",  3, 4, "sci_func"),
        # Row 4: 数字 7-9
        ("7",    4, 0, "number"), ("8",    4, 1, "number"),
        ("9",    4, 2, "number"), ("÷",    4, 3, "operator"),
        ("%",    4, 4, "func"),
        # Row 5: 数字 4-6
        ("4",    5, 0, "number"), ("5",    5, 1, "number"),
        ("6",    5, 2, "number"), ("×",    5, 3, "operator"),
        ("±",    5, 4, "func"),
        # Row 6: 数字 1-3
        ("1",    6, 0, "number"), ("2",    6, 1, "number"),
        ("3",    6, 2, "number"), ("−",    6, 3, "operator"),
        ("",     6, 4, ""),
        # Row 7: 0 . = +
        ("0",    7, 0, "number"), (".",    7, 1, "number"),
        ("=",    7, 2, "equals"), ("+",    7, 3, "operator"),
        ("",     7, 4, ""),
    ]

    # ---- 程序员模式按钮布局（5列x7行） --------------------------
    BUTTONS_PROGRAMMER = [
        # Row 0: 括号 & 清除
        ("(",    0, 0, "paren"),  (")",    0, 1, "paren"),
        ("CE",   0, 2, "func"),   ("C",    0, 3, "func"),
        ("←",    0, 4, "func"),
        # Row 1: 位运算
        ("AND",  1, 0, "bitwise"), ("OR",   1, 1, "bitwise"),
        ("XOR",  1, 2, "bitwise"), ("NOT",  1, 3, "bitwise"),
        ("%",    1, 4, "func"),
        # Row 2: 移位 & 十六进制 A-C
        ("LSH",  2, 0, "bitwise"), ("RSH",  2, 1, "bitwise"),
        ("A",    2, 2, "hex_digit"), ("B",   2, 3, "hex_digit"),
        ("C",    2, 4, "hex_digit"),
        # Row 3: 十六进制 D-F & 数字 7-8
        ("D",    3, 0, "hex_digit"), ("E",   3, 1, "hex_digit"),
        ("F",    3, 2, "hex_digit"), ("7",   3, 3, "number"),
        ("8",    3, 4, "number"),
        # Row 4: 数字 9 & 4-6
        ("9",    4, 0, "number"), ("4",    4, 1, "number"),
        ("5",    4, 2, "number"), ("6",    4, 3, "number"),
        ("×",    4, 4, "operator"),
        # Row 5: 数字 1-3
        ("÷",    5, 0, "operator"), ("1",   5, 1, "number"),
        ("2",    5, 2, "number"), ("3",    5, 3, "number"),
        ("−",    5, 4, "operator"),
        # Row 6: + ± 0 . =
        ("+",    6, 0, "operator"), ("±",   6, 1, "func"),
        ("0",    6, 2, "number"), (".",    6, 3, "number"),
        ("=",    6, 4, "equals"),
    ]

    # ── 窗口尺寸（每种模式不同） ─────────────────────────────
    GEOMETRIES = {
        "standard":   "340x600",
        "scientific": "430x680",
        "programmer": "430x760",
    }

    # ──────────────────────────────────────────────────────
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("计算器")
        self.root.geometry(self.GEOMETRIES["standard"])
        self.root.configure(bg=self.BG_DARK)
        self.root.resizable(False, False)

        # 设置窗口图标（尝试使用 Windows 内置图标）
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.btn_frame = None
        self.current_buttons = {}
        self.memory_buttons = {}
        self.base_buttons = {}
        self.mode_frame = None
        self.memory_indicator = None
        self.angle_frame = None
        self.base_panel_frame = None
        self.base_labels = {}

        self._init_state()
        self._build_display()
        self._build_mode_selector()
        self._build_memory_row()
        self._rebuild_buttons()
        self._bind_keys()
        self._update_display()

    # ═══════════════════════════════════════════════════════
    #  状态管理
    # ═══════════════════════════════════════════════════════

    def _init_state(self):
        """重置全部计算器状态（保留记忆值和模式）"""
        self.current = "0"              # 当前显示内容
        self.history_text = ""          # 历史表达式
        self.first_operand = 0.0        # 第一个操作数
        self.operator = ""              # 运算符: + − × ÷
        self.second_operand = 0.0       # 第二个操作数（用于重复=）
        self.last_operator = ""         # 上次运算符（用于重复=）
        self.new_number = True          # 下一数字键是否替换显示
        self.just_evaluated = False     # 是否刚按过 =
        self.error_state = False        # 是否处于错误状态

        # 模式状态（保留当前模式不变）
        if not hasattr(self, "mode"):
            self.mode = "standard"          # "standard" | "scientific" | "programmer"

        # 记忆状态（跨重置保留）
        if not hasattr(self, "memory"):
            self.memory = 0.0               # 存储的记忆值
            self.memory_has_value = False   # 记忆是否有值

        # 科学模式状态
        self.angle_unit = "DEG"             # "DEG" | "RAD"
        self.paren_stack = []               # 括号栈: list of (first_operand, operator, history_text)

        # 程序员模式状态
        self.base = 10                      # 当前进制: 10 | 16 | 8 | 2
        self.bit_width = 64                 # 位宽: 8 | 16 | 32 | 64

    def _format_num(self, value: float) -> str:
        """将浮点数格式化为最多15位有效数字的字符串，去除尾部零。
        在程序员模式下格式化为整数。"""
        if self.mode == "programmer":
            try:
                return str(int(value))
            except (ValueError, OverflowError):
                return "0"
        if value == 0.0:
            return "0"
        s = f"{value:.15g}"
        if len(s) > 16:
            s = f"{value:.10g}"
        return s

    def _get_display_num(self) -> float:
        """将 current 字符串安全转为 float"""
        try:
            return float(self.current)
        except ValueError:
            return 0.0

    # ═══════════════════════════════════════════════════════
    #  UI 构建
    # ═══════════════════════════════════════════════════════

    def _build_display(self):
        """构建双行显示区域"""
        display_frame = tk.Frame(self.root, bg=self.BG_DARK)
        display_frame.pack(fill=tk.BOTH, padx=4, pady=(12, 4),
                           ipady=0, expand=False)
        display_frame.configure(height=120)

        # 历史行
        self.history_label = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 12),
            fg=self.HIST_FG,
            bg=self.BG_DARK,
            anchor="e",
            justify="right",
        )
        self.history_label.pack(fill=tk.X, padx=20, pady=(30, 2))

        # 当前行（大字体）
        self.current_label = tk.Label(
            display_frame,
            text="0",
            font=("Segoe UI", 28, "bold"),
            fg=self.FG_WHITE,
            bg=self.BG_DARK,
            anchor="e",
            justify="right",
        )
        self.current_label.pack(fill=tk.X, padx=20, pady=(0, 8))

    def _build_mode_selector(self):
        """构建模式切换按钮行"""
        self.mode_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.mode_frame.pack(fill=tk.X, padx=12, pady=(2, 0))

        modes = [
            ("标准", "standard"),
            ("科学", "scientific"),
            ("程序员", "programmer"),
        ]

        for (label, mode_id) in modes:
            btn = tk.Button(
                self.mode_frame,
                text=label,
                font=("Segoe UI", 10),
                fg=self.FG_WHITE,
                bg=self.FUNC_BG,
                activeforeground=self.FG_WHITE,
                activebackground=self.OP_BG,
                relief=tk.FLAT,
                bd=1,
                padx=10,
                pady=2,
                cursor="hand2",
                command=lambda m=mode_id: self._switch_mode(m),
            )
            btn.pack(side=tk.LEFT, padx=2)

        # 角度单位切换（仅科学模式可见）
        self.angle_frame = tk.Frame(self.mode_frame, bg=self.BG_DARK)

        tk.Label(
            self.angle_frame,
            text=" ",
            font=("Segoe UI", 10),
            fg=self.HIST_FG,
            bg=self.BG_DARK,
        ).pack(side=tk.LEFT, padx=(12, 0))

        for unit in ("DEG", "RAD"):
            btn = tk.Button(
                self.angle_frame,
                text=unit,
                font=("Segoe UI", 9),
                fg=self.FG_WHITE,
                bg=self.FUNC_BG,
                activeforeground=self.FG_WHITE,
                activebackground=self.OP_BG,
                relief=tk.FLAT,
                bd=1,
                padx=6,
                pady=2,
                cursor="hand2",
                command=lambda u=unit: self._set_angle_unit(u),
            )
            btn.pack(side=tk.LEFT, padx=1)

    def _build_memory_row(self):
        """构建记忆功能按钮行"""
        mem_frame = tk.Frame(self.root, bg=self.BG_DARK)
        mem_frame.pack(fill=tk.X, padx=12, pady=(4, 0))

        # 记忆值指示器
        self.memory_indicator = tk.Label(
            mem_frame,
            text="",
            font=("Segoe UI", 8),
            fg=self.OP_BG,
            bg=self.BG_DARK,
            anchor="w",
        )
        self.memory_indicator.pack(side=tk.LEFT, padx=(4, 0))

        # 记忆按钮 (从右到左排列)
        mem_labels = ["MC", "MR", "M+", "M-", "MS"]
        for label in reversed(mem_labels):
            btn = tk.Button(
                mem_frame,
                text=label,
                font=("Segoe UI", 10),
                fg=self.FG_WHITE,
                bg=self.BG_DARK,
                activeforeground=self.FG_WHITE,
                activebackground=self.FUNC_HOVER,
                relief=tk.FLAT,
                bd=1,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda t=label: self._on_click(t),
            )
            btn.pack(side=tk.RIGHT, padx=1)
            self.memory_buttons[label] = btn

        self._update_memory_indicator()

    def _build_standard_grid(self):
        """构建标准模式 6行×4列 按钮网格"""
        self.btn_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.btn_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # 行/列权重均匀分配
        for i in range(6):
            self.btn_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.btn_frame.columnconfigure(j, weight=1)

        # 颜色映射
        color_map = self._get_color_map()

        self.current_buttons = {}

        for (text, row, col, btype) in self.BUTTONS:
            c = color_map[btype]
            btn = tk.Button(
                self.btn_frame,
                text=text,
                font=("Segoe UI", 14),
                fg=self.FG_WHITE,
                bg=c["bg"],
                activeforeground=self.FG_WHITE,
                activebackground=c["hover"],
                relief=tk.FLAT,
                bd=1,
                padx=2,
                pady=2,
                cursor="hand2",
                command=lambda t=text: self._on_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

            # 悬停变色
            btn.bind("<Enter>",
                     lambda e, b=btn, hc=c["hover"]: b.configure(bg=hc))
            btn.bind("<Leave>",
                     lambda e, b=btn, bc=c["bg"]: b.configure(bg=bc))

            self.current_buttons[text] = btn

    def _get_color_map(self):
        """返回按钮类型到颜色配置的映射"""
        return {
            "func":     {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
            "operator": {"bg": self.OP_BG,    "hover": self.OP_HOVER},
            "number":   {"bg": self.NUM_BG,   "hover": self.NUM_HOVER},
            "equals":   {"bg": self.OP_BG,    "hover": self.OP_HOVER},
            "memory":   {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
            "sci_func": {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
            "paren":    {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
            "bitwise":  {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
            "hex_digit":{"bg": self.NUM_BG,   "hover": self.NUM_HOVER},
            "base_sel": {"bg": self.FUNC_BG,  "hover": self.FUNC_HOVER},
        }

    def _rebuild_buttons(self):
        """销毁旧按钮网格并重建当前模式对应的布局"""
        if self.btn_frame is not None:
            self.btn_frame.destroy()
            self.btn_frame = None
        self.current_buttons = {}

        if self.mode == "standard":
            self._build_standard_grid()
        elif self.mode == "scientific":
            self._build_scientific_grid()
        elif self.mode == "programmer":
            self._build_programmer_grid()

    def _switch_mode(self, new_mode: str):
        """切换计算器模式"""
        if new_mode == self.mode:
            return

        prev_mode = self.mode
        self.mode = new_mode

        # 显示/隐藏角度单位选择
        if self.mode == "scientific":
            self.angle_frame.pack(side=tk.LEFT)
        else:
            self.angle_frame.pack_forget()

        # 离开程序员模式时隐藏进制面板
        if prev_mode == "programmer" and self.base_panel_frame is not None:
            self.base_panel_frame.pack_forget()

        # 调整窗口大小
        self.root.geometry(self.GEOMETRIES[self.mode])

        # 重置计算状态
        self._init_state()
        self._rebuild_buttons()

        # 进入程序员模式时显示进制面板
        if self.mode == "programmer":
            if self.base_panel_frame is None:
                self._build_base_panel()
            else:
                self.base_panel_frame.pack(
                    fill=tk.X, padx=12, pady=(2, 0),
                    before=self.btn_frame
                )
            self._update_base_display()

        self._update_display()

    def _set_angle_unit(self, unit: str):
        """设置角度单位（仅科学模式）"""
        self.angle_unit = unit

    def _build_scientific_grid(self):
        """科学模式 5列×8行 按钮网格"""
        self.btn_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.btn_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        for i in range(8):
            self.btn_frame.rowconfigure(i, weight=1)
        for j in range(5):
            self.btn_frame.columnconfigure(j, weight=1)

        color_map = self._get_color_map()
        self.current_buttons = {}

        for (text, row, col, btype) in self.BUTTONS_SCIENTIFIC:
            if not text:  # skip empty placeholders
                continue
            c = color_map.get(btype, color_map["func"])
            btn = tk.Button(
                self.btn_frame, text=text,
                font=("Segoe UI", 13),
                fg=self.FG_WHITE, bg=c["bg"],
                activeforeground=self.FG_WHITE, activebackground=c["hover"],
                relief=tk.FLAT, bd=1, padx=2, pady=2, cursor="hand2",
                command=lambda t=text: self._on_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            btn.bind("<Enter>",
                     lambda e, b=btn, hc=c["hover"]: b.configure(bg=hc))
            btn.bind("<Leave>",
                     lambda e, b=btn, bc=c["bg"]: b.configure(bg=bc))
            self.current_buttons[text] = btn

    def _build_programmer_grid(self):
        """程序员模式 5列×7行 按钮网格"""
        self.btn_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.btn_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        for i in range(7):
            self.btn_frame.rowconfigure(i, weight=1)
        for j in range(5):
            self.btn_frame.columnconfigure(j, weight=1)

        color_map = self._get_color_map()
        self.current_buttons = {}

        for (text, row, col, btype) in self.BUTTONS_PROGRAMMER:
            if not text:
                continue
            c = color_map.get(btype, color_map["func"])
            btn = tk.Button(
                self.btn_frame, text=text,
                font=("Segoe UI", 13),
                fg=self.FG_WHITE, bg=c["bg"],
                activeforeground=self.FG_WHITE, activebackground=c["hover"],
                relief=tk.FLAT, bd=1, padx=2, pady=2, cursor="hand2",
                command=lambda t=text: self._on_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            btn.bind("<Enter>",
                     lambda e, b=btn, hc=c["hover"]: b.configure(bg=hc))
            btn.bind("<Leave>",
                     lambda e, b=btn, bc=c["bg"]: b.configure(bg=bc))
            self.current_buttons[text] = btn

        # 初始更新数字按钮状态（根据当前进制）
        self._update_digit_states()

    def _bind_keys(self):
        """绑定键盘事件"""
        self.root.bind("<KeyPress>", self._on_key)
        self.root.bind("<Return>", lambda e: self._on_click("="))
        self.root.bind("<BackSpace>", lambda e: self._on_click("←"))
        self.root.bind("<Escape>", lambda e: self._on_click("C"))
        self.root.bind("<Delete>", lambda e: self._on_click("CE"))
        self.root.focus_set()

    # ═══════════════════════════════════════════════════════
    #  键盘处理
    # ═══════════════════════════════════════════════════════

    def _on_key(self, event: tk.Event):
        """键盘按键映射到按钮"""
        key = event.char.lower() if event.char else ""
        key_upper = key.upper()

        mapping = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            ".": ".", "%": "%",
            "+": "+", "-": "−", "*": "×", "/": "÷",
        }
        if key in mapping:
            self._on_click(mapping[key])
            return

        # 十六进制 A-F
        if self.mode == "programmer" and key_upper in "ABCDEF":
            self._on_click(key_upper)
            return

        # 科学模式额外快捷键
        if self.mode == "scientific":
            sci_keys = {
                "s": "sin", "c": "cos", "t": "tan",
                "l": "log", "n": "ln",
                "p": "π",
            }
            if key in sci_keys:
                self._on_click(sci_keys[key])
                return

        # 括号
        if key == "(":
            self._on_click("(")
        elif key == ")":
            self._on_click(")")

        # Backspace（已在 _bind_keys 中绑定）
        # Enter（已在 _bind_keys 中绑定）

    # ═══════════════════════════════════════════════════════
    #  点击分发
    # ═══════════════════════════════════════════════════════

    def _on_click(self, text: str):
        """统一按钮点击分发器"""
        if text in "0123456789":
            self._digit(text)
        elif text in "ABCDEF":
            self._digit(text)
        elif text == ".":
            self._decimal()
        elif text in ("+", "−", "×", "÷"):
            self._operator(text)
        elif text == "=":
            self._equals()
        elif text == "C":
            self._clear_all()
        elif text == "CE":
            self._clear_entry()
        elif text == "←":
            self._backspace()
        elif text == "±":
            self._negate()
        elif text == "%":
            self._percent()
        elif text == "1/x":
            self._reciprocal()
        elif text == "x²":
            self._square()
        elif text == "√x":
            self._sqrt()

        # ── 记忆功能 ──
        elif text == "MC":
            self._memory_clear()
        elif text == "MR":
            self._memory_recall()
        elif text == "M+":
            self._memory_add()
        elif text == "M-":
            self._memory_subtract()
        elif text == "MS":
            self._memory_store()

        # ── 科学功能 ──
        elif text == "sin":
            self._sin()
        elif text == "cos":
            self._cos()
        elif text == "tan":
            self._tan()
        elif text == "log":
            self._log()
        elif text == "ln":
            self._ln()
        elif text == "10^x":
            self._ten_power_x()
        elif text == "e^x":
            self._exp()
        elif text == "n!":
            self._factorial()
        elif text == "π":
            self._pi()
        elif text == "e":
            self._e_constant()
        elif text == "x^y":
            self._operator("^")
        elif text == "y√x":
            self._operator("y√x")
        elif text == "(":
            self._left_paren()
        elif text == ")":
            self._right_paren()

        # ── 程序员功能 ──
        elif text == "AND":
            self._operator("&")
        elif text == "OR":
            self._operator("|")
        elif text == "XOR":
            self._operator("prog^")
        elif text == "NOT":
            self._bitwise_not()
        elif text == "LSH":
            self._operator("<<")
        elif text == "RSH":
            self._operator(">>")

        self._update_display()

    # ═══════════════════════════════════════════════════════
    #  数字输入
    # ═══════════════════════════════════════════════════════

    def _digit(self, digit: str):
        """处理数字键输入（含十六进制）"""
        if self.error_state:
            return

        # 程序员模式：检查该数字是否允许
        if self.mode == "programmer":
            allowed = {
                16: set("0123456789ABCDEF"),
                10: set("0123456789"),
                8:  set("01234567"),
                2:  set("01"),
            }.get(self.base, set("0123456789"))
            if digit not in allowed:
                return

        if self.just_evaluated:
            self._init_state()
        if self.new_number:
            self.current = digit
            self.new_number = False
        else:
            if self.current == "0":
                self.current = digit
            else:
                # 程序员模式限制8位（64-bit limitation）
                max_len = 16 if self.mode != "programmer" else 16
                s = self.current.replace("-", "").replace(".", "")
                if len(s) < max_len:
                    self.current += digit
        self.just_evaluated = False

        # 程序员模式：自动更新进制面板
        if self.mode == "programmer":
            self._update_base_display()

    def _decimal(self):
        """处理小数点"""
        if self.error_state:
            return
        if self.just_evaluated:
            self._init_state()
        if self.new_number:
            self.current = "0."
            self.new_number = False
        else:
            if "." not in self.current:
                self.current += "."
        self.just_evaluated = False

    # ═══════════════════════════════════════════════════════
    #  运算符处理
    # ═══════════════════════════════════════════════════════

    def _operator(self, op: str):
        """处理运算符键 (+ − × ÷)"""
        if self.error_state:
            return

        current_val = self._get_display_num()

        if self.just_evaluated:
            # 刚按过 =，用结果作为第一操作数继续
            self.first_operand = current_val
            self.history_text = f"{self._format_num(current_val)} {op}"
            self.operator = op
            self.new_number = True
            self.just_evaluated = False
            return

        if self.operator and not self.new_number:
            # 有待处理运算：先计算上一轮
            second = current_val
            result, err = self._compute(self.first_operand, self.operator, second)
            if err:
                self._show_error(err)
                return
            self.first_operand = result
            self.current = self._format_num(result)
            self.history_text = f"{self._format_num(result)} {op}"
        else:
            self.first_operand = current_val
            self.history_text = f"{self._format_num(current_val)} {op}"

        self.operator = op
        self.new_number = True
        self.just_evaluated = False

    # ═══════════════════════════════════════════════════════
    #  等号处理
    # ═══════════════════════════════════════════════════════

    def _equals(self):
        """处理等号键"""
        if self.error_state:
            return

        current_val = self._get_display_num()

        # 重复按等号：重复上次运算
        if self.just_evaluated and self.last_operator:
            first = current_val
            second = self.second_operand
            op = self.last_operator
            self.history_text = (
                f"{self._format_num(first)} {op} "
                f"{self._format_num(second)} ="
            )
            result, err = self._compute(first, op, second)
            if err:
                self._show_error(err)
                return
            self.current = self._format_num(result)
            self.first_operand = result
            self.just_evaluated = True
            self.new_number = True
            return

        # 无运算符 → 直接显示当前值
        if not self.operator:
            self.history_text = f"{self._format_num(current_val)} ="
            self.first_operand = current_val
            self.just_evaluated = True
            self.new_number = True
            return

        # 正常计算
        second = current_val
        self.history_text = (
            f"{self._format_num(self.first_operand)} {self.operator} "
            f"{self._format_num(second)} ="
        )
        result, err = self._compute(self.first_operand, self.operator, second)
        if err:
            self._show_error(err)
            return

        # 保存用于重复等号
        self.second_operand = second
        self.last_operator = self.operator

        self.current = self._format_num(result)
        self.first_operand = result
        self.operator = ""
        self.just_evaluated = True
        self.new_number = True

    # ═══════════════════════════════════════════════════════
    #  功能键
    # ═══════════════════════════════════════════════════════

    def _clear_all(self):
        """C 键：全部清除"""
        self._init_state()

    def _clear_entry(self):
        """CE 键：清除当前输入"""
        if self.error_state:
            self._init_state()
            return
        self.current = "0"
        self.new_number = True

    def _backspace(self):
        """← 键：退格删除最后一位"""
        if self.error_state:
            return
        if self.new_number:
            return
        if len(self.current) > 1:
            self.current = self.current[:-1]
            # 处理只剩负号的情况
            if self.current == "-":
                self.current = "0"
                self.new_number = True
        else:
            self.current = "0"
            self.new_number = True

    def _negate(self):
        """± 键：正负号切换"""
        if self.error_state:
            return
        if self.current == "0":
            return
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current

    def _percent(self):
        """% 键：百分比（除以100）"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.current = self._format_num(val / 100.0)

    def _reciprocal(self):
        """1/x 键：倒数"""
        if self.error_state:
            return
        val = self._get_display_num()
        if val == 0.0:
            self._show_error("无效输入")
            return
        self.current = self._format_num(1.0 / val)

    def _square(self):
        """x² 键：平方"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.current = self._format_num(val * val)

    def _sqrt(self):
        """√x 键：平方根"""
        if self.error_state:
            return
        val = self._get_display_num()
        if val < 0:
            self._show_error("无效输入")
            return
        self.current = self._format_num(math.sqrt(val))

    # ═══════════════════════════════════════════════════════
    #  记忆功能
    # ═══════════════════════════════════════════════════════

    def _memory_clear(self):
        """MC: 清除记忆值"""
        self.memory = 0.0
        self.memory_has_value = False
        self._update_memory_indicator()

    def _memory_recall(self):
        """MR: 调用记忆值"""
        if self.error_state:
            return
        if not self.memory_has_value:
            return
        self.current = self._format_num(self.memory)
        self.new_number = True
        self.just_evaluated = False

    def _memory_add(self):
        """M+: 当前值加到记忆"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.memory += val
        self.memory_has_value = True
        self.new_number = True
        self._update_memory_indicator()

    def _memory_subtract(self):
        """M-: 从记忆中减去当前值"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.memory -= val
        self.memory_has_value = True
        self.new_number = True
        self._update_memory_indicator()

    def _memory_store(self):
        """MS: 存储当前值到记忆"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.memory = val
        self.memory_has_value = True
        self.new_number = True
        self._update_memory_indicator()

    def _update_memory_indicator(self):
        """更新记忆指示器显示"""
        if self.memory_indicator is not None:
            if self.memory_has_value:
                self.memory_indicator.configure(text="●")
            else:
                self.memory_indicator.configure(text="")

    # ═══════════════════════════════════════════════════════
    #  科学计算
    # ═══════════════════════════════════════════════════════

    def _sin(self):
        """正弦函数"""
        if self.error_state:
            return
        val = self._get_display_num()
        if self.angle_unit == "DEG":
            val = math.radians(val)
        self.current = self._format_num(math.sin(val))
        self.new_number = True

    def _cos(self):
        """余弦函数"""
        if self.error_state:
            return
        val = self._get_display_num()
        if self.angle_unit == "DEG":
            val = math.radians(val)
        self.current = self._format_num(math.cos(val))
        self.new_number = True

    def _tan(self):
        """正切函数"""
        if self.error_state:
            return
        val = self._get_display_num()
        if self.angle_unit == "DEG":
            val = math.radians(val)
        # 检查 cos 是否接近零（tan = sin/cos）
        cos_val = math.cos(val)
        if abs(cos_val) < 1e-12:
            self._show_error("无效输入")
            return
        self.current = self._format_num(math.tan(val))
        self.new_number = True

    def _log(self):
        """常用对数 (log10)"""
        if self.error_state:
            return
        val = self._get_display_num()
        if val <= 0:
            self._show_error("无效输入")
            return
        self.current = self._format_num(math.log10(val))
        self.new_number = True

    def _ln(self):
        """自然对数"""
        if self.error_state:
            return
        val = self._get_display_num()
        if val <= 0:
            self._show_error("无效输入")
            return
        self.current = self._format_num(math.log(val))
        self.new_number = True

    def _ten_power_x(self):
        """10^x"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.current = self._format_num(math.pow(10, val))
        self.new_number = True

    def _exp(self):
        """e^x"""
        if self.error_state:
            return
        val = self._get_display_num()
        self.current = self._format_num(math.exp(val))
        self.new_number = True

    def _factorial(self):
        """阶乘 n!"""
        if self.error_state:
            return
        val = self._get_display_num()
        if val < 0 or val != int(val):
            self._show_error("无效输入")
            return
        try:
            self.current = self._format_num(float(math.factorial(int(val))))
        except (OverflowError, ValueError):
            self._show_error("溢出")
            return
        self.new_number = True

    def _pi(self):
        """插入 π 常量"""
        if self.error_state:
            return
        self.current = self._format_num(math.pi)
        self.new_number = True
        self.just_evaluated = False

    def _e_constant(self):
        """插入 e 常量"""
        if self.error_state:
            return
        self.current = self._format_num(math.e)
        self.new_number = True
        self.just_evaluated = False

    # ═══════════════════════════════════════════════════════
    #  括号处理
    # ═══════════════════════════════════════════════════════

    def _left_paren(self):
        """左括号：压栈并重置"""
        if self.error_state:
            return
        self.paren_stack.append((
            self.first_operand, self.operator, self.history_text
        ))
        self.first_operand = 0.0
        self.operator = ""
        self.history_text += " ("
        self.new_number = True
        self.just_evaluated = False

    def _right_paren(self):
        """右括号：计算当前值并弹出栈"""
        if self.error_state:
            return
        if not self.paren_stack:
            return

        current_val = self._get_display_num()

        # 如果有未完成的运算，先计算
        if self.operator:
            result, err = self._compute(
                self.first_operand, self.operator, current_val
            )
            if err:
                self._show_error(err)
                return
            current_val = result

        # 弹出保存的状态
        saved_operand, saved_op, saved_history = self.paren_stack.pop()
        self.first_operand = saved_operand
        self.operator = saved_op
        self.history_text = (
            saved_history + f" {self._format_num(current_val)}"
        )
        if not saved_op:
            self.history_text += " )"
        self.current = self._format_num(current_val)
        self.new_number = True

    # ═══════════════════════════════════════════════════════
    #  程序员模式
    # ═══════════════════════════════════════════════════════

    def _build_base_panel(self):
        """构建进制显示面板"""
        self.base_panel_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.base_panel_frame.pack(fill=tk.X, padx=12, pady=(2, 0),
                                    before=self.btn_frame)

        # 四行进制显示
        self.base_labels = {}
        for base_name in ("HEX", "DEC", "OCT", "BIN"):
            row_frame = tk.Frame(self.base_panel_frame, bg=self.BG_DARK)
            row_frame.pack(fill=tk.X)

            lbl = tk.Label(
                row_frame,
                text=f"{base_name}  0",
                font=("Segoe UI", 11),
                fg=self.HIST_FG,
                bg=self.BG_DARK,
                anchor="w",
                justify="left",
            )
            lbl.pack(side=tk.LEFT, padx=4)
            self.base_labels[base_name] = lbl

        # 进制选择按钮
        base_sel_frame = tk.Frame(self.base_panel_frame, bg=self.BG_DARK)
        base_sel_frame.pack(fill=tk.X, pady=(4, 0))

        for base in ("HEX", "DEC", "OCT", "BIN"):
            btn = tk.Button(
                base_sel_frame,
                text=base,
                font=("Segoe UI", 10),
                fg=self.FG_WHITE,
                bg=self.FUNC_BG if base != "DEC" else self.OP_BG,
                activeforeground=self.FG_WHITE,
                activebackground=self.OP_BG,
                relief=tk.FLAT,
                bd=1,
                padx=10,
                pady=2,
                cursor="hand2",
                command=lambda b=base: self._set_base(b),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.base_buttons[base] = btn

        self._update_base_display()

    def _set_base(self, base_name: str):
        """切换程序员模式进制"""
        base_map = {"HEX": 16, "DEC": 10, "OCT": 8, "BIN": 2}
        self.base = base_map[base_name]

        # 更新进制按钮颜色
        for name, btn in self.base_buttons.items():
            if name == base_name:
                btn.configure(bg=self.OP_BG)
            else:
                btn.configure(bg=self.FUNC_BG)

        # 清空当前输入
        self.current = "0"
        self.new_number = True

        # 更新数字按钮可用状态
        self._update_digit_states()
        self._update_base_display()

    def _update_digit_states(self):
        """根据当前进制启用/禁用数字按钮"""
        if self.mode != "programmer":
            return

        # 各进制允许的数字
        allowed_digits = {
            16: set("0123456789ABCDEF"),
            10: set("0123456789"),
            8:  set("01234567"),
            2:  set("01"),
        }
        allowed = allowed_digits.get(self.base, set("0123456789"))

        for text, btn in self.current_buttons.items():
            if text in "0123456789ABCDEF":
                if text in allowed:
                    btn.configure(state=tk.NORMAL,
                                  bg=self.NUM_BG)
                else:
                    btn.configure(state=tk.DISABLED,
                                  bg="#1a1a1a")

        # 小数点：仅在十进制模式可用
        if "." in self.current_buttons:
            if self.base == 10:
                self.current_buttons["."].configure(state=tk.NORMAL)
            else:
                self.current_buttons["."].configure(state=tk.DISABLED,
                                                    bg="#1a1a1a")

    def _update_base_display(self):
        """更新进制显示面板"""
        if self.base_panel_frame is None:
            return
        try:
            val = int(self._get_display_num())
        except (ValueError, OverflowError):
            val = 0

        # 按位宽截断
        mask = (1 << self.bit_width) - 1
        val = val & mask

        formats = {
            "HEX": f"HEX  {val & mask:X}",
            "DEC": f"DEC  {val & mask}",
            "OCT": f"OCT  {oct(val & mask)[2:]}",
            "BIN": f"BIN  {bin(val & mask)[2:]}",
        }
        for name, lbl in self.base_labels.items():
            lbl.configure(text=formats[name])

    def _bitwise_not(self):
        """按位取反 NOT"""
        if self.error_state:
            return
        val = int(self._get_display_num())
        mask = (1 << self.bit_width) - 1
        result = (~val) & mask
        # 直接设为整数字符串，避免浮点精度丢失
        self.current = str(result)
        self.new_number = True
        self._update_base_display()

    # ═══════════════════════════════════════════════════════
    #  核心计算
    # ═══════════════════════════════════════════════════════

    def _compute(self, a: float, op: str, b: float) -> tuple:
        """
        执行四则运算及扩展运算
        返回 (result, error_message)
        成功时 error_message 为空字符串
        """
        if op == "+":
            return (a + b, "")
        elif op == "−":
            return (a - b, "")
        elif op == "×":
            return (a * b, "")
        elif op == "÷":
            if b == 0.0:
                return (0.0, "除数不能为零")
            return (a / b, "")
        elif op == "^":
            # x^y: 幂运算
            if a < 0 and b != int(b):
                return (0.0, "无效输入")
            return (math.pow(a, b), "")
        elif op == "y√x":
            # y√x: 开方运算 (a是根指数, b是被开方数)
            if a == 0:
                return (0.0, "无效输入")
            if b < 0 and int(a) % 2 == 0:
                return (0.0, "无效输入")
            return (math.pow(b, 1.0 / a), "")
        elif op == "&":
            return (float(int(a) & int(b)), "")
        elif op == "|":
            return (float(int(a) | int(b)), "")
        elif op == "prog^":
            return (float(int(a) ^ int(b)), "")
        elif op == "<<":
            return (float(int(a) << int(b)), "")
        elif op == ">>":
            return (float(int(a) >> int(b)), "")
        return (0.0, f"未知运算符: {op}")

    def _show_error(self, msg: str):
        """显示错误信息"""
        self.current = msg
        self.error_state = True
        self.history_text = ""

    # ═══════════════════════════════════════════════════════
    #  显示更新
    # ═══════════════════════════════════════════════════════

    def _update_display(self):
        """同步刷新双行显示及进制面板"""
        self.history_label.configure(text=self.history_text)

        display_text = self.current
        # 限制显示长度
        if len(display_text) > 20 and not self.error_state:
            display_text = display_text[:20]

        # 错误状态用红色
        if self.error_state:
            self.current_label.configure(fg=self.ERR_FG)
        else:
            self.current_label.configure(fg=self.FG_WHITE)

        self.current_label.configure(text=display_text)

        # 更新记忆指示器
        self._update_memory_indicator()

        # 程序员模式：更新进制显示
        if self.mode == "programmer":
            self._update_base_display()

    # ═══════════════════════════════════════════════════════
    #  启动
    # ═══════════════════════════════════════════════════════

    def run(self):
        """启动计算器主循环"""
        self.root.mainloop()


# ── 入口 ──────────────────────────────────────────────────
if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
