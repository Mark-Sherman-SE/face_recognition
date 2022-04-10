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
        db = DB()
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
        tk.Button(self.root, text="Войти по логину", command=lambda : PasswordPage(login=self.login.get(), db=DB), width=50, height=1).grid(row=3, column=1)
        tk.Button(self.root, text="Войти по камере", command=lambda: CameraPage(self.mtcnn, self.model, 11, db=DB, login=self.login.get()),
                  width=50, height=1).grid(row=4, column=1)

        self.root.mainloop()
        db.cursor.close()


MainPage()
