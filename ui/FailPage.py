import tkinter as tk

class FailPage:
    def __init__(self, err_obj="login"):
        window = tk.Toplevel()
        window.grab_set()
        window.title(f"Wrong {err_obj}")

        tk.Label(window, text=f"Try another {err_obj}", width=50,compound=tk.CENTER).grid(row=0, column=0)
