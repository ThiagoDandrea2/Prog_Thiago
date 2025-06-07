import tkinter as tk
from tkinter import font
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Elegant Tkinter Calculator")
        self.configure(bg="#ffffff")
        self.geometry("400x600")
        self.resizable(False, False)

        # Fonts for a modern look, using system font stack
        self.large_bold_font = font.Font(family="Inter, Arial, sans-serif", size=32, weight="bold")
        self.button_font = font.Font(family="Inter, Arial, sans-serif", size=18, weight="bold")
        self.display_font = font.Font(family="Inter, Arial, sans-serif", size=40, weight="bold")

        # Container frame with padding and white background for card effect
        container = tk.Frame(self, bg="#ffffff", padx=32, pady=32)
        container.pack(expand=True, fill="both")

        # Display frame with subtle background and rounded corners effect
        display_frame = tk.Frame(container, bg="#f9fafb", bd=0, highlightthickness=0, relief="flat")
        display_frame.pack(fill="both", pady=(0, 32))

        # Display label for current expression/result
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            font=self.display_font,
            bg="#f9fafb",
            fg="#111827",  # very dark gray (almost black)
            relief="flat",
            padx=16,
            pady=24,
            wraplength=380,  # prevent overflow
            justify="right"
        )
        self.display.pack(fill="both")

        # Button colors and styles for consistent look
        self.btn_bg = "#e5e7eb"        # light gray for numbers
        self.btn_fg = "#374151"        # dark gray for text
        self.btn_bg_active = "#d1d5db" # slightly darker on press
        self.btn_special_bg = "#111827"    # black for operators and special buttons
        self.btn_special_fg = "#f9fafb"    # white for button text in special buttons

        # A frame to hold all buttons
        buttons_frame = tk.Frame(container, bg="#ffffff")
        buttons_frame.pack(fill="both")

        # Memory state
        self.memory = None

        # Buttons layout with extended functions
        buttons = [
            # Memory buttons row
            ("MC", 0, 0, self.memory_clear),
            ("MR", 0, 1, self.memory_recall),
            ("M+", 0, 2, self.memory_add),
            ("M-", 0, 3, self.memory_subtract),
            
            # Clear and sign toggle row
            ("AC", 1, 0, self.all_clear),
            ("C", 1, 1, self.clear),
            ("±", 1, 2, self.toggle_sign),
            ("÷", 1, 3, lambda: self.press_operator("/")),

            # Numbers and operators rows
            ("7", 2, 0, lambda: self.press_num("7")),
            ("8", 2, 1, lambda: self.press_num("8")),
            ("9", 2, 2, lambda: self.press_num("9")),
            ("×", 2, 3, lambda: self.press_operator("*")),

            ("4", 3, 0, lambda: self.press_num("4")),
            ("5", 3, 1, lambda: self.press_num("5")),
            ("6", 3, 2, lambda: self.press_num("6")),
            ("−", 3, 3, lambda: self.press_operator("-")),

            ("1", 4, 0, lambda: self.press_num("1")),
            ("2", 4, 1, lambda: self.press_num("2")),
            ("3", 4, 2, lambda: self.press_num("3")),
            ("+", 4, 3, lambda: self.press_operator("+")),

            ("0", 5, 0, lambda: self.press_num("0")),
            (".", 5, 1, lambda: self.press_num(".")),
            ("%", 5, 2, self.percent),
            ("=", 5, 3, self.calculate),

            # Extra functions row (sqrt and power)
            ("√", 6, 0, self.square_root),
            ("x²", 6, 1, self.square),
            ("^", 6, 2, lambda: self.press_operator("**")),
            ("", 6, 3, None),  # placeholder for grid consistency
        ]

        # Create the buttons in grid, some spanning columns (0 except "0" spans 2)
        for (text, row, col, cmd) in buttons:
            if text == "":
                # Spacer, skip
                continue
            if text == "0":
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    command=cmd,
                    font=self.button_font,
                    bg=self.btn_bg,
                    fg=self.btn_fg,
                    activebackground=self.btn_bg_active,
                    activeforeground=self.btn_fg,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=20,
                    borderwidth=0,
                )
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=8, pady=8)
            elif text == "=":
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    command=cmd,
                    font=self.button_font,
                    bg="#2563eb",  # blue for = button
                    fg="#f9fafb",
                    activebackground="#1e40af",
                    activeforeground="#f9fafb",
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=20,
                    borderwidth=0,
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            elif text in ("+", "−", "×", "÷", "AC", "C", "±", "%", "√", "x²", "^", "MC", "MR", "M+", "M-"):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    command=cmd,
                    font=self.button_font,
                    bg=self.btn_special_bg,
                    fg=self.btn_special_fg,
                    activebackground="#1f2937",
                    activeforeground=self.btn_special_fg,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=20,
                    borderwidth=0,
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            else:
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    command=cmd,
                    font=self.button_font,
                    bg=self.btn_bg,
                    fg=self.btn_fg,
                    activebackground=self.btn_bg_active,
                    activeforeground=self.btn_fg,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=0,
                    pady=20,
                    borderwidth=0,
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        # Configure grid weights for responsive equal spacing
        total_rows = 7
        for i in range(total_rows):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)

        # Internal variables
        self.current_expression = ""
        self.last_pressed_equal = False

    # Number button press handler
    def press_num(self, num):
        if self.last_pressed_equal:
            self.current_expression = ""
            self.last_pressed_equal = False
        if num == ".":
            if self.current_expression == "" or self.current_expression[-1] in "+-*/**":
                self.current_expression += "0."
            elif "." in self._get_last_number():
                return
            else:
                self.current_expression += "."
        else:
            self.current_expression += num
        self.display_var.set(self.current_expression)

    # Get last contiguous number for dot validations
    def _get_last_number(self):
        tokens = []
        for ch in reversed(self.current_expression):
            if ch in "+-*/":
                break
            tokens.append(ch)
        return "".join(reversed(tokens))

    # Operator button press handler
    def press_operator(self, op):
        if self.current_expression == "":
            if op == "-":
                self.current_expression = "-"
                self.display_var.set(self.current_expression)
            return
        # For exponentiation we may have "**" so handle appropriately
        if op == "**":
            if self.current_expression.endswith("**"):
                return
            elif self.current_expression[-1] in "+-*/":
                self.current_expression = self.current_expression[:-1] + op
            else:
                self.current_expression += op
            self.display_var.set(self.current_expression)
            self.last_pressed_equal = False
            return

        if self.current_expression[-1] in "+-*/":
            self.current_expression = self.current_expression[:-1] + op
        else:
            self.current_expression += op
        self.display_var.set(self.current_expression)
        self.last_pressed_equal = False

    # Clear last entry
    def clear(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            if self.current_expression == "":
                self.display_var.set("0")
            else:
                self.display_var.set(self.current_expression)

    # All Clear resets everything
    def all_clear(self):
        self.current_expression = ""
        self.display_var.set("0")
        self.last_pressed_equal = False

    # Toggle sign +/-
    def toggle_sign(self):
        if self.current_expression == "":
            return
        try:
            # Evaluate current number for toggling
            # Find last number and replace it with negated version
            last_number = self._get_last_number()
            if last_number == "":
                return
            last_index = self.current_expression.rfind(last_number)
            negated = str(-float(last_number))
            self.current_expression = self.current_expression[:last_index] + negated
            self.display_var.set(self.current_expression)
        except Exception:
            return

    # Percentage function: divide by 100
    def percent(self):
        try:
            if self.current_expression == "":
                return
            value = eval(self.current_expression)
            value = value / 100
            self.current_expression = str(value)
            self.display_var.set(self.current_expression)
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""

    # Square root function
    def square_root(self):
        try:
            if self.current_expression == "":
                return
            value = eval(self.current_expression)
            if value < 0:
                self.display_var.set("Error")
                self.current_expression = ""
                return
            result = math.sqrt(value)
            self.current_expression = str(result)
            self.display_var.set(self.current_expression)
            self.last_pressed_equal = True
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""

    # Square function x²
    def square(self):
        try:
            if self.current_expression == "":
                return
            value = eval(self.current_expression)
            result = value * value
            self.current_expression = str(result)
            self.display_var.set(self.current_expression)
            self.last_pressed_equal = True
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""

    # Calculator equals button
    def calculate(self):
        try:
            # Safely evaluate the arithmetic expression
            expression = self.current_expression.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
            result = eval(expression)
            # Formatting floats properly
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display_var.set(str(result))
            self.current_expression = str(result)
            self.last_pressed_equal = True
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""
            self.last_pressed_equal = True

    # Memory operations
    def memory_clear(self):
        self.memory = None

    def memory_recall(self):
        if self.memory is not None:
            if self.last_pressed_equal:
                self.current_expression = ""
                self.last_pressed_equal = False
            self.current_expression += str(self.memory)
            self.display_var.set(self.current_expression)

    def memory_add(self):
        try:
            if self.current_expression == "":
                return
            value = eval(self.current_expression)
            if self.memory is None:
                self.memory = value
            else:
                self.memory += value
            self.last_pressed_equal = True
            self.display_var.set(str(self.memory))
            self.current_expression = str(self.memory)
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""

    def memory_subtract(self):
        try:
            if self.current_expression == "":
                return
            value = eval(self.current_expression)
            if self.memory is None:
                self.memory = -value
            else:
                self.memory -= value
            self.last_pressed_equal = True
            self.display_var.set(str(self.memory))
            self.current_expression = str(self.memory)
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

