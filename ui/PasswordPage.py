import tkinter
import tkinter as tk

from DB import DB
from ui.FailPage import FailPage
from ui.SuccessPage import SuccessPage


class PasswordPage:
    def __init__(self, login: str, db: DB):
        self.db = db
        self.window = tkinter.Toplevel()
        self.window.grab_set()
        self.window.title("Password")
        tk.Label(self.window, text="Enter Password").grid(row=0, column=1)
        self.password = tk.StringVar()
        tk.Entry(self.window, textvariable=self.password, width=50).grid(row=1, column=1)
        tk.Button(self.window, text="Войти", command=lambda: self.login(login=login, password=self.password.get()),
                  width=50,
                  height=1).grid(row=2, column=1)

    def login(self, login, password):
        s = f"SELECT password FROM sqlitedb WHERE login='{login}'"

        self.db.cursor.execute(s)
        pwd = self.db.cursor.fetchone()[0]

        s = f"SELECT name FROM sqlitedb WHERE login='{login}'"

        self.db.cursor.execute(s)
        name = self.db.cursor.fetchone()[0]
        if password == pwd:
            SuccessPage(name=name)
        else:
            print(pwd)
            print(password)
            FailPage(err_obj="password")
