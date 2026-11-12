"""Cross-platform tkinter calculator (Python standard library only)."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from calcxx.engine import CalculatorError, evaluate_expression, format_result
from calcxx.history import History


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("calcXX — Scientific Desk")
        self.geometry("510x675")
        self.minsize(430, 590)
        self.configure(bg="#10182a")
        self.history = History()
        self.expression = tk.StringVar(value="")
        self.status = tk.StringVar(value="Ready · all calculations stay on this device")
        self._build()
        self.bind("<Return>", lambda _: self.calculate())
        self.bind("<Escape>", lambda _: self.expression.set(""))

    def _build(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="#152540", foreground="#eaf2ff",
                        fieldbackground="#152540", rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#243d5a", foreground="#d3e9fa")
        heading = tk.Label(self, text="calcXX", bg="#10182a", fg="#80e6cb",
                           font=("Arial", 28, "bold"))
        heading.pack(anchor="w", padx=23, pady=(22, 1))
        tk.Label(self, text="Precise arithmetic  /  Scientific functions",
                 bg="#10182a", fg="#9cb6cb", font=("Arial", 11)).pack(anchor="w", padx=24)
        entry = tk.Entry(self, textvariable=self.expression, bg="#192c48", fg="#f2fbff",
                         insertbackground="white", font=("Consolas", 21), relief="flat",
                         highlightthickness=2, highlightbackground="#345073")
        entry.pack(fill="x", padx=22, pady=(21, 8), ipady=14)
        entry.focus_set()
        layout = [
            ["7", "8", "9", "/", "sqrt("],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", ".", "pi", "+", "^"],
            ["sin(", "cos(", "tan(", "ln(", "log10("],
        ]
        panel = tk.Frame(self, bg="#10182a")
        panel.pack(fill="x", padx=19)
        for row, keys in enumerate(layout):
            for col, key in enumerate(keys):
                bg = "#234261" if key in {"/", "*", "-", "+", "^"} else "#1b304b"
                button = tk.Button(panel, text=key, bg=bg, fg="#f0f7fd", activebackground="#335a7a",
                                   activeforeground="white", relief="flat", font=("Arial", 12, "bold"),
                                   command=lambda value=key: self.expression.set(self.expression.get() + value))
                button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew", ipady=8)
        for col in range(5):
            panel.grid_columnconfigure(col, weight=1)
        actions = tk.Frame(self, bg="#10182a")
        actions.pack(fill="x", padx=20, pady=(7, 9))
        for label, function, bg in [
            ("Clear", lambda: self.expression.set(""), "#314359"),
            ("⌫ Delete", self.backspace, "#314359"),
            ("= Calculate", self.calculate, "#39c6a6"),
        ]:
            tk.Button(actions, text=label, command=function, bg=bg,
                      fg="#061c22" if label.startswith("=") else "#e7f3fc",
                      font=("Arial", 11, "bold"), relief="flat").pack(side="left", expand=True, fill="x", padx=3, ipady=9)
        tk.Label(self, textvariable=self.status, bg="#10182a", fg="#aad3db", wraplength=460,
                 justify="left").pack(anchor="w", padx=24, pady=(0, 8))
        tk.Label(self, text="RECENT CALCULATIONS", bg="#10182a",
                 fg="#80e6cb", font=("Arial", 10, "bold")).pack(anchor="w", padx=24)
        self.list = tk.Listbox(self, bg="#152540", fg="#ecf5fb", selectbackground="#265a6c",
                               relief="flat", font=("Consolas", 10), height=6)
        self.list.pack(fill="both", expand=True, padx=23, pady=(8, 18))
        self.list.bind("<Double-Button-1>", self.reuse)

    def backspace(self):
        self.expression.set(self.expression.get()[:-1])

    def calculate(self):
        expression = self.expression.get()
        try:
            value = format_result(evaluate_expression(expression))
        except CalculatorError as error:
            self.status.set("Check expression: " + str(error))
            return
        self.history.record(expression, value)
        self.expression.set(value)
        self.status.set("Calculated locally · Enter to calculate, Esc to clear")
        self.list.delete(0, tk.END)
        for original, answer in self.history.items:
            self.list.insert(tk.END, f"{original} = {answer}")

    def reuse(self, _event):
        selected = self.list.curselection()
        if selected:
            self.expression.set(self.history.items[selected[0]][0])


if __name__ == "__main__":
    Calculator().mainloop()
