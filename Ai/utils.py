import os
import cv2

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise Exception(f"Cannot load image: {path}")
    return img

def save_image(path, img):
    cv2.imwrite(path, img)
