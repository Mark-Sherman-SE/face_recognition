import tkinter as tk

class SuccessPage:
    def __init__(self):
        window = tk.Toplevel()
        window.grab_set()
        window.title("Success")

        tk.Label(window, text="УРА", width=50,compound=tk.CENTER).grid(row=0, column=0)
