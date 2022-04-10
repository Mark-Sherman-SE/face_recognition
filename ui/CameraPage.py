import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import torch
import time

from DB import DB
from .SuccessPage import SuccessPage
from torchvision import transforms
from constants import DEVICE


class CameraPage:
    def __init__(self, mtcnn, model, face_id,login, db:DB, video_source=0):
        self.db=db
        s = f"SELECT id FROM sqlitedb WHERE login={login}"

        self.db.cursor.execute(s)
        self.face_id = self.db.cursor.fetchone()
        s = f"SELECT name FROM sqlitedb WHERE login={login}"

        self.db.cursor.execute(s)
        self. name= self.db.cursor.fetchone()

        self.window = tkinter.Toplevel()
        self.window.grab_set()
        self.window.title("Camera")

        self.video_source = video_source
        # self.face_id = face_id
        self.mtcnn = mtcnn
        self.model = model
        self.counter = 0

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()


        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.transformation = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        self.update()

        self.window.mainloop()


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            face = self.mtcnn(frame)
            if face is not None:
                face_t = self.transformation(face)
                face_t = face_t.to(DEVICE).unsqueeze(0)
                pred = self.model(face_t)
                _, id = torch.max(pred, 1)
                self.counter += int(self.face_id == id)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

                if self.counter == 5:
                    SuccessPage(name=self.name)
        self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return None
            # return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
