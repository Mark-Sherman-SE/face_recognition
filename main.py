import tkinter as tk
import os

from ui.CameraPage import CameraPage
from ui.SuccessPage import SuccessPage

from nn.models.mtcnn import MTCNN
from nn.models.inception_resnet_v1 import InceptionResnetV1

from constants import *


class MainPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.grab_set()
        self.login = tk.StringVar()
        tk.Entry(self.root, textvariable=self.login, width=50).grid(row=0, column=1)
        self.password = tk.StringVar()
        self.mtcnn = MTCNN(
            image_size=160, margin=0, min_face_size=20,
            thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
            device=DEVICE
        )
        data_dir = os.path.join(DATA_ALIGNED, "test")
        directories = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
        self.model = InceptionResnetV1(classify=True, pretrained='vggface2', num_classes=len(directories)).to(DEVICE)
        self.model.load_state_dict(torch.load("result/weights/best_weights.pth"))
        self.model.eval()
        tk.Entry(self.root, textvariable=self.password, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="Войти по логину", command=self.login_password, width=50, height=1).grid(row=3, column=1)
        tk.Button(self.root, text="Войти по камере", command=lambda: CameraPage(self.mtcnn, self.model, 11),
                  width=50, height=1).grid(row=4, column=1)

        self.root.mainloop()

    def login_password(self):
        if self.login.get() == "123" and self.password.get() == "123":
            SuccessPage()

MainPage()
