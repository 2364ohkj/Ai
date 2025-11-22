import cv2
import os

def smooth(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if len(files) < 2:
        print("⚠️ Smoothing 스킵 — 프레임이 2개 미만입니다.")
        return input_dir

    prev = cv2.imread(os.path.join(input_dir, files[0]))
    out_path = os.path.join(output_dir, files[0])
    cv2.imwrite(out_path, prev)

    for i in range(1, len(files)):
        curr = cv2.imread(os.path.join(input_dir, files[i]))

        # 80% previous + 20% current → 부드럽게 변화하는 프레임
        blended = cv2.addWeighted(prev, 0.8, curr, 0.2, 0)

        out_path = os.path.join(output_dir, files[i])
        cv2.imwrite(out_path, blended)

        prev = blended

    return output_dir
