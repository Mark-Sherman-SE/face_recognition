import tkinter as tk

class FailPage:
    def __init__(self):
        window = tk.Toplevel()
        window.grab_set()
        window.title("Wrong login")

        tk.Label(window, text=f"Try another login", width=50,compound=tk.CENTER).grid(row=0, column=0)
