import tkinter as tk
from tkinter import font

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Elegant Tkinter Calculator")
        self.configure(bg="#ffffff")
        self.geometry("360x520")
        self.resizable(False, False)

        # Fonts
        self.large_bold_font = font.Font(family="Inter", size=28, weight="bold")
        self.button_font = font.Font(family="Inter", size=18, weight="bold")
        self.display_font = font.Font(family="Inter", size=36, weight="bold")

        # Main container frame with padding and bg to create card effect
        container = tk.Frame(self, bg="#ffffff", padx=24, pady=24)
        container.pack(expand=True, fill="both")

        # Display frame (card style with subtle shadow)
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        display_frame = tk.Frame(container, bg="#f9fafb", bd=0, highlightthickness=0)
        display_frame.pack(fill="both", pady=(0, 24))

        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            font=self.display_font,
            bg="#f9fafb",
            fg="#111827",  # almost black
            relief="flat",
            padx=12,
            pady=20
        )
        self.display.pack(fill="both")

        # Button colors
        self.btn_bg = "#e5e7eb"  # light gray
        self.btn_fg = "#374151"  # dark gray text
        self.btn_bg_active = "#d1d5db"
        self.btn_special_bg = "#111827"  # black for special buttons
        self.btn_special_fg = "#f9fafb"  # white text

        # Buttons container
        buttons_frame = tk.Frame(container, bg="#ffffff")
        buttons_frame.pack(fill="both")

        # Buttons text and layout (like iOS calculator style)
        buttons = [
            ("C", 1, 0, self.clear),
            ("÷", 1, 3, lambda: self.press_operator("/")),
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
            ("=", 5, 2, self.calculate),
        ]

        # Create buttons
        for (text, row, col, cmd) in buttons:
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
                    highlightbackground="#000000"
                )
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=8, pady=8)
            elif text == "=":
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
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=8 if col==2 else 0, pady=8)
            elif text in ("+", "−", "×", "÷", "C"):
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

        # Configure grid weights for responsiveness
        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)

        # Internal variables to track input
        self.current_expression = ""
        self.last_pressed_equal = False

    def press_num(self, num):
        if self.last_pressed_equal:
            # Reset expression if last was equal and number pressed
            self.current_expression = ""
            self.last_pressed_equal = False
        # Prevent multiple dots in a number
        if num == ".":
            if self.current_expression == "" or self.current_expression[-1] in "+-*/":
                self.current_expression += "0."
            elif "." in self._get_last_number():
                return
            else:
                self.current_expression += "."
        else:
            self.current_expression += num
        self.display_var.set(self.current_expression)

    def _get_last_number(self):
        # Helper to get the last number segment for dot validation
        tokens = []
        for ch in reversed(self.current_expression):
            if ch in "+-*/":
                break
            tokens.append(ch)
        return "".join(reversed(tokens))

    def press_operator(self, op):
        if self.current_expression == "":
            # Do not allow operator at the beginning except minus for negative
            if op == "-":
                self.current_expression = "-"
                self.display_var.set(self.current_expression)
            return
        if self.current_expression[-1] in "+-*/":
            # Replace last operator with new one
            self.current_expression = self.current_expression[:-1] + op
        else:
            self.current_expression += op
        self.display_var.set(self.current_expression)
        self.last_pressed_equal = False

    def clear(self):
        self.current_expression = ""
        self.display_var.set("0")
        self.last_pressed_equal = False

    def calculate(self):
        try:
            # Replace unicode operators with python operators
            expression = self.current_expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            # Evaluate expression safely
            result = eval(expression)
            # Format result removing trailing zeros for float
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display_var.set(str(result))
            self.current_expression = str(result)
            self.last_pressed_equal = True
        except Exception:
            self.display_var.set("Error")
            self.current_expression = ""
            self.last_pressed_equal = True

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

