import cv2
import os
import numpy as np

# 개별 이미지 노이즈 제거
def denoise_image(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

# 폴더 단위 처리
def process_denoise(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    file_list = sorted(os.listdir(input_dir))
    out_files = []

    for f in file_list:
        path = os.path.join(input_dir, f)
        img = cv2.imread(path)

        if img is None:
            print(f"⚠️ 이미지 불러오기 실패: {path}")
            continue

        cleaned = denoise_image(img)
        out_path = os.path.join(output_dir, f)
        cv2.imwrite(out_path, cleaned)
        out_files.append(out_path)

    return output_dir
