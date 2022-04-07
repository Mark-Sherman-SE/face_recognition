import tkinter as tk

from ui.CameraPage import CameraPage
from ui.SuccessPage import SuccessPage


class MainPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.grab_set()
        self.login = tk.StringVar()
        tk.Entry(self.root, textvariable=self.login, width=50).grid(row=0, column=1)
        self.password = tk.StringVar()
        tk.Entry(self.root, textvariable=self.password, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="Войти по логину", command=self.login_password, width=50, height=1).grid(row=3, column=1)
        tk.Button(self.root, text="Войти по камере", command=lambda: CameraPage(), width=50, height=1).grid(row=4, column=1)

        self.root.mainloop()

    def login_password(self):
        if self.login.get() == "123" and self.password.get() == "123":
            SuccessPage()

MainPage()
