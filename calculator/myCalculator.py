"""
myCalculator

A desktop GUI calculator built with Python and Tkinter for CSC426.
The whole expression you type is shown in the display, and the answer is
added after you press = (for example 2+4-93=-87). It supports + - * / \\ ^ %
with normal operator precedence, plus Clear and backspace.

Run it:
    python3 myCalculator.py
"""

import math
import tkinter as tk

OPERATORS = set("+-*/\\^%")


# --------- expression evaluator (recursive descent, respects precedence) ---------
class Parser:
    def __init__(self, text):
        self.s = text
        self.i = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def take(self):
        ch = self.s[self.i]
        self.i += 1
        return ch

    def parse(self):
        value = self.expression()
        if self.i < len(self.s):
            raise ValueError("unexpected input")
        return value

    def expression(self):          # + and -
        x = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            y = self.term()
            x = x + y if op == "+" else x - y
        return x

    def term(self):                # * / \ %
        x = self.power()
        while self.peek() in ("*", "/", "\\", "%"):
            op = self.take()
            y = self.power()
            if op == "*":
                x = x * y
            elif op == "/":
                if y == 0:
                    raise ZeroDivisionError("divide by zero")
                x = x / y
            elif op == "\\":
                if y == 0:
                    raise ZeroDivisionError("divide by zero")
                x = math.floor(x / y)
            else:                  # %
                if y == 0:
                    raise ZeroDivisionError("mod by zero")
                x = x % y
        return x

    def power(self):               # ^  (right associative)
        base = self.unary()
        if self.peek() == "^":
            self.take()
            exponent = self.power()
            return base ** exponent
        return base

    def unary(self):
        if self.peek() == "-":
            self.take()
            return -self.unary()
        if self.peek() == "+":
            self.take()
            return self.unary()
        return self.number()

    def number(self):
        start = self.i
        while self.i < len(self.s) and (self.s[self.i].isdigit() or self.s[self.i] == "."):
            self.i += 1
        if start == self.i:
            raise ValueError("number expected")
        return float(self.s[start:self.i])


def evaluate(text):
    result = Parser(text).parse()
    if not isinstance(result, (int, float)) or result != result or result in (float("inf"), float("-inf")):
        raise ValueError("undefined")
    return result


def format_result(value):
    if value == int(value):
        return str(int(value))
    return str(value)


# ------------------------------- the calculator UI -------------------------------
class MyCalculator:
    BG = "#fdf0f2"
    SURFACE = "#ffffff"
    BORDER = "#f0d6db"
    TEXT = "#2a1f22"
    MUTED = "#7a6066"
    OP_BG = "#fde2e7"
    OP_FG = "#c41f3e"
    FUNC_BG = "#f6e7ea"
    CLEAR_FG = "#b3261e"
    EQ_BG = "#e63950"

    def __init__(self, root):
        self.root = root
        self.expr = ""
        self.evaluated = False

        root.title("myCalculator")
        root.configure(bg=self.BG)
        root.geometry("600x400")
        root.minsize(520, 360)

        self.shown = tk.StringVar(value="0")
        self.build_display()
        self.build_keypad()
        self.bind_keys()

    def build_display(self):
        wrap = tk.Frame(self.root, bg=self.BG)
        wrap.pack(fill="x", padx=14, pady=(14, 8))
        entry = tk.Entry(
            wrap, textvariable=self.shown, justify="right", state="readonly",
            readonlybackground=self.SURFACE, fg=self.TEXT,
            font=("Consolas", 26), relief="solid", bd=1, highlightthickness=0,
        )
        entry.pack(fill="x", ipady=16)

    def build_keypad(self):
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        rows = [
            ["Clear", "<-", "%", "\\", "^"],
            ["7", "8", "9", "/", "*"],
            ["4", "5", "6", "-", "+"],
            ["1", "2", "3", "0", "."],
        ]
        for c in range(5):
            body.grid_columnconfigure(c, weight=1, uniform="keys")
        for r in range(len(rows) + 1):
            body.grid_rowconfigure(r, weight=1, uniform="keys")

        for r, row in enumerate(rows):
            for c, label in enumerate(row):
                self.make_button(body, label).grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        equals = self.make_button(body, "=", equals=True)
        equals.grid(row=len(rows), column=0, columnspan=5, sticky="nsew", padx=4, pady=4)

    def make_button(self, parent, label, equals=False):
        if equals:
            bg, fg = self.EQ_BG, "#ffffff"
        elif label == "Clear":
            bg, fg = self.FUNC_BG, self.CLEAR_FG
        elif label == "<-":
            bg, fg = self.FUNC_BG, self.MUTED
        elif label in OPERATORS:
            bg, fg = self.OP_BG, self.OP_FG
        else:
            bg, fg = self.SURFACE, self.TEXT

        return tk.Button(
            parent, text=label, command=lambda t=label: self.on_press(t),
            bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
            font=("Segoe UI", 16), relief="flat", bd=0,
            highlightbackground=self.BORDER, highlightthickness=1, cursor="hand2",
        )

    # ------------------------------- input handling -------------------------------
    def on_press(self, token):
        if token == "Clear":
            self.clear()
        elif token == "<-":
            self.backspace()
        elif token in ("=", "Enter"):
            self.equals()
        elif token == ".":
            self.dot()
        elif token in OPERATORS:
            self.operator(token)
        else:
            self.digit(token)

    def clear(self):
        self.expr = ""
        self.evaluated = False
        self.shown.set("0")

    def digit(self, d):
        if self.evaluated:
            self.expr = d
            self.evaluated = False
        else:
            self.expr += d
        self.show()

    def dot(self):
        if self.evaluated:
            self.expr = "0."
            self.evaluated = False
        elif self.expr == "" or self.expr[-1] in OPERATORS:
            self.expr += "0."
        elif not self.last_number_has_dot():
            self.expr += "."
        self.show()

    def operator(self, op):
        if self.evaluated:
            self.evaluated = False
        if self.expr == "":
            if op == "-":
                self.expr = "-"
        elif self.expr[-1] in OPERATORS:
            self.expr = self.expr[:-1] + op
        else:
            self.expr += op
        self.show()

    def backspace(self):
        if self.evaluated:
            self.expr = ""
            self.evaluated = False
        elif self.expr:
            self.expr = self.expr[:-1]
        self.show()

    def equals(self):
        if self.expr == "" or self.expr[-1] in OPERATORS:
            return
        try:
            result = format_result(evaluate(self.expr))
            self.shown.set(self.expr + "=" + result)
            self.expr = result
            self.evaluated = True
        except Exception:
            self.shown.set("Error")
            self.expr = ""
            self.evaluated = False

    def last_number_has_dot(self):
        for ch in reversed(self.expr):
            if ch in OPERATORS:
                return False
            if ch == ".":
                return True
        return False

    def show(self):
        self.shown.set(self.expr if self.expr else "0")

    def bind_keys(self):
        self.root.bind("<Key>", self.on_key)
        self.root.bind("<Return>", lambda e: self.on_press("="))
        self.root.bind("<BackSpace>", lambda e: self.on_press("<-"))
        self.root.bind("<Escape>", lambda e: self.on_press("Clear"))

    def on_key(self, event):
        ch = event.char
        if ch.isdigit() or ch in OPERATORS or ch == ".":
            self.on_press(ch)
        elif ch == "=":
            self.on_press("=")


if __name__ == "__main__":
    window = tk.Tk()
    MyCalculator(window)
    window.mainloop()
