import cv2
import os
import numpy as np

# 개별 이미지 색보정 함수
def color_grade_image(img):
    # LAB 밝기 조절
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 약한 톤매핑
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l2 = clahe.apply(l)

    merged = cv2.merge((l2, a, b))
    graded = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    return graded

# 폴더 단위 색보정
def color_grade(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = sorted(os.listdir(input_dir))
    out_paths = []

    for f in files:
        in_path = os.path.join(input_dir, f)
        if not os.path.isfile(in_path):
            continue

        img = cv2.imread(in_path)
        if img is None:
            print(f"⚠️ 이미지 로드 실패: {in_path}")
            continue

        graded = color_grade_image(img)
        out_path = os.path.join(output_dir, f)
        cv2.imwrite(out_path, graded)

        out_paths.append(out_path)

    return output_dir
