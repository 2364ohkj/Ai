#!/usr/bin/env python3
import os
import glob
import argparse

from moviepy import VideoFileClip, concatenate_videoclips
from Ai.interpolate.veo_transition_vertex import generate_transition_vertex


def merge_videos(clips, output_file, fps=30):
    """여러 개 mp4 클립을 하나로 이어 붙임."""
    if not clips:
        print("⚠ 병합할 클립이 없음")
        return

    video_clips = []
    try:
        for c in clips:
            if not os.path.exists(c):
                print(f"⚠ 클립 없음, 스킵: {c}")
                continue
            video_clips.append(VideoFileClip(c))

        if not video_clips:
            print("⚠ 유효한 클립이 하나도 없음")
            return

        final = concatenate_videoclips(video_clips, method="compose")
        final.write_videofile(output_file, fps=fps)
    finally:
        for vc in video_clips:
            vc.close()


def run_demo_v2(
    frames_dir: str,
    output_file: str = "final.mp4",
    out_dir: str = "demo_out",
    resume: bool = True,
):
    """
    frames_dir 안의 jpg 이미지를 순서대로 읽어서
    인접한 두 장씩 Veo 전환 영상을 만들고,
    마지막에 하나로 병합.
    """
    print("🚀 Veo 기반 이미지 전환 영상 생성 시작")

    images = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))
    if len(images) < 2:
        print(f"❌ 최소 2장 필요 (현재 {len(images)}장)")
        return

    os.makedirs(out_dir, exist_ok=True)

    clips = []
    num_pairs = len(images) - 1

    for i in range(num_pairs):
        imgA, imgB = images[i], images[i + 1]
        out_clip = os.path.join(out_dir, f"transition_{i+1:04d}.mp4")

        # 이미 만들어둔 클립이면 스킵 (resume 용)
        if resume and os.path.exists(out_clip) and os.path.getsize(out_clip) > 0:
            print(f"⏭ [{i+1}/{num_pairs}] 이미 존재, 스킵 → {out_clip}")
        else:
            print(f"🎬 [{i+1}/{num_pairs}] {os.path.basename(imgA)} → {os.path.basename(imgB)}")
            try:
                generate_transition_vertex(imgA, imgB, out_clip)
            except Exception as e:
                print(f"❌ 전환 생성 실패: {imgA} -> {imgB}")
                print("   ", e)
                # 실패한 구간은 스킵
                continue

        clips.append(out_clip)

    if not clips:
        print("⚠ 생성된/사용 가능한 클립 없음. 종료.")
        return

    print("📎 클립 병합 중…")
    merge_videos(clips, output_file)
    print("🎉 최종 영상 생성 완료:", output_file)


def main():
    parser = argparse.ArgumentParser(
        description="로드뷰 프레임으로 Veo 전환 영상 생성"
    )
    parser.add_argument(
        "--frames_dir",
        required=True,
        help="입력 프레임(jpg)들이 들어있는 디렉토리",
    )
    parser.add_argument(
        "--output",
        default="final.mp4",
        help="최종 출력 영상 파일 이름 (기본: final.mp4)",
    )
    parser.add_argument(
        "--out_dir",
        default="demo_out",
        help="중간 transition 클립 저장 디렉토리 (기본: demo_out)",
    )
    parser.add_argument(
        "--no_resume",
        action="store_true",
        help="이미 존재하는 transition_*.mp4도 다시 생성하고 싶으면 사용",
    )

    args = parser.parse_args()

    run_demo_v2(
        frames_dir=args.frames_dir,
        output_file=args.output,
        out_dir=args.out_dir,
        resume=not args.no_resume,
    )


if __name__ == "__main__":
    main()
