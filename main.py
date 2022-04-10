import tkinter as tk
import os

from DB import DB
from ui.CameraPage import CameraPage
from ui.PasswordPage import PasswordPage

from nn.models.mtcnn import MTCNN
from nn.models.inception_resnet_v1 import InceptionResnetV1

from constants import *


class MainPage:
    def __init__(self):
        self.db = DB()
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.grab_set()
        self.login = tk.StringVar()
        tk.Entry(self.root, textvariable=self.login, width=50).grid(row=0, column=1)
        self.mtcnn = MTCNN(
            image_size=160, margin=0, min_face_size=20,
            thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
            device=DEVICE
        )
        data_dir = os.path.join(DATA_ALIGNED, "test")
        directories = [0]*12#[name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
        self.model = InceptionResnetV1(classify=True, pretrained='vggface2', num_classes=len(directories)).to(DEVICE)
        self.model.load_state_dict(torch.load("result/weights/best_weights.pth"))
        self.model.eval()
        tk.Button(self.root, text="Войти по логину", command=lambda :self.check_login(login=self.login.get(), mode=True), width=50, height=1).grid(row=3, column=1)
        tk.Button(self.root, text="Войти по камере", command=lambda: self.check_login(login=self.login.get(), mode=False),
                  width=50, height=1).grid(row=4, column=1)

        self.root.mainloop()
        self.db.cursor.close()

    def check_login(self, login, mode):
        try:
            s = f"SELECT id FROM sqlitedb WHERE login={login}"

            self.db.cursor.execute(s)
            self.db.cursor.fetchone()

            if mode:
                PasswordPage(login=login, db=self.db)
            else:
                CameraPage(self.mtcnn, self.model, 11, db=self.db, login=login)


        except:
            print("Wrong login")



MainPage()
