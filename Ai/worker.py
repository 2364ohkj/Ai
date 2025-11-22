import os
from utils import ensure_dir, load_image, save_image
from preprocess.brightness import fix_brightness
from preprocess.denoise import denoise
from interpolate.rife_runner import run_rife
from postprocess.color_grade import color_grade
from video.render import render_video

def process_job(job_id, frames_dir, output_video):
    print(f"AI Worker: Start job {job_id}")

    # 1) 전처리
    clean_dir = f"{frames_dir}_clean"
    ensure_dir(clean_dir)

    for f in sorted(os.listdir(frames_dir)):
        path = os.path.join(frames_dir, f)
        img = load_image(path)

        img = fix_brightness(img)
        img = denoise(img)

        save_image(os.path.join(clean_dir, f), img)

    # 2) 보간
    interp_dir = f"{frames_dir}_interp"
    ensure_dir(interp_dir)

    run_rife(clean_dir, interp_dir, num=4)

    # 3) 후처리
    final_dir = f"{frames_dir}_final"
    ensure_dir(final_dir)

    for f in sorted(os.listdir(interp_dir)):
        path = os.path.join(interp_dir, f)
        img = load_image(path)

        img = color_grade(img)
        save_image(os.path.join(final_dir, f), img)

    # 4) 영상 렌더링
    render_video(final_dir, output_video)

    print(f"AI Worker: Finished job {job_id}")
    return output_video
