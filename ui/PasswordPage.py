import tkinter
import tkinter as tk

from ui.SuccessPage import SuccessPage


class PasswordPage:
    def __init__(self,login:str):
        self.window = tkinter.Toplevel()
        self.window.grab_set()
        self.window.title("Password")
        tk.Label(self.window, text="Enter Password").grid(row=0, column=1)
        self.password = tk.StringVar()
        tk.Entry(self.window, textvariable=self.password, width=50).grid(row=1, column=1)
        tk.Button(self.window, text="Войти", command=lambda: self.login(login=login, password=self.password.get()), width=50,
                  height=1).grid(row=2, column=1)

    def login(self, login, password):
        if login =="123" and password=="123":
            SuccessPage()