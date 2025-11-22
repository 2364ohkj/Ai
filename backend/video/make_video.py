import cv2
import os
import argparse
import natsort


def make_video(input_dir, output_file, fps=30):
    files = [f for f in os.listdir(input_dir) if f.endswith(".jpg")]
    if not files:
        print("❌ No frames found")
        return

    files = natsort.natsorted(files)
    first = cv2.imread(os.path.join(input_dir, files[0]))
    h, w, _ = first.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_file, fourcc, fps, (w, h))

    for f in files:
        frame = cv2.imread(os.path.join(input_dir, f))
        video.write(frame)

    video.release()
    print(f"🎬 Video created → {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    make_video(args.input, args.output, args.fps)
