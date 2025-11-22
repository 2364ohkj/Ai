import os
import base64
import json
import requests

API_KEY = os.environ.get("GOOGLE_API_KEY")
MODEL_ID = "veo-1.5"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateVideo?key={API_KEY}"

def generate_transition(imgA, imgB, output_path):
    print(f"🌀 Veo REST API transition: {imgA} → {imgB}")

    if API_KEY is None:
        print("❌ GOOGLE_API_KEY 환경변수가 없습니다!")
        return

    def encode(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    imgA_b64 = encode(imgA)
    imgB_b64 = encode(imgB)

    payload = {
        "prompt": "smooth cinematic transition between two images",
        "images": [
            {"data": imgA_b64, "mime_type": "image/jpeg"},
            {"data": imgB_b64, "mime_type": "image/jpeg"}
        ],
        "video_config": {
            "fps": 24,
            "duration_seconds": 2
        }
    }

    response = requests.post(ENDPOINT, json=payload)
    if response.status_code != 200:
        print("❌ API 오류:")
        print(response.text)
        return None

    data = response.json()

    video_b64 = data["video"]["data"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(video_b64))

    print("✅ Transition 영상 생성 완료:", output_path)
    return output_path
