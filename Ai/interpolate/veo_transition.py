import os
import google.genai as genai

MODEL_ID = "veo-3.0-fast"


def generate_transition(imgA, imgB, output_path, project=None):
    print(f"🌀 Veo 3 transition 생성 중: {imgA} → {imgB}")

    # 1) 클라이언트 초기화
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    # 2) 이미지 로드
    with open(imgA, "rb") as f:
        imgA_bytes = f.read()

    with open(imgB, "rb") as f:
        imgB_bytes = f.read()

    # 3) 영상 생성
    result = client.models.generate_videos(
        model=MODEL_ID,
        contents=[
            {
                "mime_type": "image/jpeg",
                "data": imgA_bytes
            },
            {
                "mime_type": "image/jpeg",
                "data": imgB_bytes
            },
        ],
        generation_config={
            "duration_seconds": 2,   # 2초 transition
            "fps": 24
        }
    )

    # 4) 결과 저장
    video_bytes = result.videos[0].data

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(video_bytes)

    print("✅ Transition 완료:", output_path)
