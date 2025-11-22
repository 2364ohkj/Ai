import cv2
import numpy as np
import os

# 기존: 이미지 1장에 대한 밝기 보정
def fix_brightness(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    out = cv2.merge((cl, a, b))
    return cv2.cvtColor(out, cv2.COLOR_LAB2BGR)


# 🔥 새로 추가: 폴더 단위 밝기 보정
def process_brightness(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = sorted(os.listdir(input_dir))
    out_files = []

    for f in files:
        if not f.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        input_path = os.path.join(input_dir, f)
        output_path = os.path.join(output_dir, f)

        img = cv2.imread(input_path)
        if img is None:
            print(f"⚠️ 이미지 불러오기 실패: {input_path}")
            continue

        out = fix_brightness(img)
        cv2.imwrite(output_path, out)
        out_files.append(output_path)

    return output_dir
