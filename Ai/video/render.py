import cv2

def merge_videos(video_list, output_path):
    if not video_list:
        return

    # 첫 영상 기준 정보
    cap = cv2.VideoCapture(video_list[0])
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    for v in video_list:
        cap = cv2.VideoCapture(v)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()

    out.release()
    print("✔ merged video saved:", output_path)
