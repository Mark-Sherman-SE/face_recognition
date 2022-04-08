import numpy as np
import cv2
import glob
import os
import shutil
import pathlib
from autocrop import Cropper
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from sklearn.model_selection import train_test_split


def get_test_transform():
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def get_train_transform():
    return transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.ColorJitter(brightness=0.5, contrast=0.5),
        transforms.RandomRotation(degrees=(-5, 5)),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def process_video(path, person_name, save_path, test_size=0.25, info=False):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0
    num_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    test_frames = np.random.choice(num_of_frames, int(test_size * num_of_frames), replace=False) + count

    for subfolder in ["test", "train"]:
        if os.path.isdir(os.path.join(save_path, subfolder, person_name)):
            files = glob.glob(os.path.join(save_path, subfolder, person_name, "/*.jpg"))
            for file in files:
                try:
                    index = int(file.split("_")[-1])
                except ValueError:
                    continue
                count = index if index > count else count

    if success:
        pathlib.Path(f"{save_path}\\test\\{person_name}").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{save_path}\\train\\{person_name}").mkdir(parents=True, exist_ok=True)
    while success:
        folder = "test" if count in test_frames else "train"
        is_written = cv2.imwrite(f"{save_path}\\{folder}\\{person_name}\\{person_name}_{str(format(count, '04d'))}.jpg",
                                image)
        if info:
            print('Read a new frame: ', count, is_written)
        success, image = vidcap.read()
        count += 1


def crop_images(person_name, train_path, test_path, target_dir="data/default/"):
    train_paths = glob.glob(os.path.join(train_path, f"{person_name}/*.jpg"))
    test_paths = glob.glob(os.path.join(test_path, f"{person_name}/*.jpg"))
    cropper = Cropper()

    for sub_dir, cur_path in [["train", train_paths], ["test", test_paths]]:
        if len(cur_path) > 0:
            pathlib.Path(os.path.join(target_dir, sub_dir, person_name)).mkdir(parents=True, exist_ok=True)
            for file in cur_path:
                cropped_image = cropper.crop(file)
                if cropped_image.size != 0:
                    cv2.imwrite(os.path.join(target_dir, sub_dir, person_name, os.path.basename(file)), cropped_image)


def relocate_images(input_path, output_path, is_traget_dir_train, test_size=0.25):
    directories = [name for name in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, name))]
    for dir in directories:
        images = os.listdir(os.path.join(input_path, dir))
        train, test = train_test_split(images, test_size=test_size)
        target_images = train if is_traget_dir_train else test
        for image in target_images:
            pathlib.Path(os.path.join(output_path, dir)).mkdir(parents=True, exist_ok=True)
            shutil.move(os.path.join(input_path, dir, image), os.path.join(output_path, dir))


class Flatten(nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return x


class Normalize(nn.Module):
    def __init__(self):
        super(Normalize, self).__init__()

    def forward(self, x):
        x = F.normalize(x, p=2, dim=1)
        return x
