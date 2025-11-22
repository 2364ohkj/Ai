import os
from imagen_interpolate import generate_middle_frame

def generate_interpolated_sequence(input_dir, output_dir, num_ai_frames=7):
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([
        x for x in os.listdir(input_dir)
        if x.lower().endswith((".jpg",".png",".jpeg"))
    ])

    full_output = []
    counter = 0

    for i in range(len(files) - 1):
        f1 = os.path.join(input_dir, files[i])
        f2 = os.path.join(input_dir, files[i+1])

        # 원본 프레임 저장
        out_original = os.path.join(output_dir, f"{counter:05d}.jpg")
        os.system(f"cp '{f1}' '{out_original}'")
        full_output.append(out_original)
        counter += 1

        # AI 중간 프레임 생성
        for j in range(num_ai_frames):
            out_mid = os.path.join(output_dir, f"{counter:05d}.jpg")
            generate_middle_frame(f1, f2, out_mid)
            full_output.append(out_mid)
            counter += 1

    return output_dir
