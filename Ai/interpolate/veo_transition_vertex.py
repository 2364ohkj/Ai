import base64
from google import genai

MODEL_ID = "veo-video-001"       # 최신 Vertex Veo 모델
LOCATION = "us-central1"         # Veo 지원 리전

def generate_transition_vertex(imgA_path, imgB_path, output_path):
    print(f"🌀 Veo transition 생성 중: {imgA_path} → {imgB_path}")

    # Vertex AI 인증 기반 클라이언트
    client = genai.Client(
        vertexai=True,
        project="verdant-oven-479008-q3",
        location=LOCATION,
    )

    # 이미지 읽어서 base64 인코딩
    def load_img(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    imgA_b64 = load_img(imgA_path)
    imgB_b64 = load_img(imgB_path)

    prompt = """
        Create a smooth video transition blending Image A into Image B.
        Make it cinematic and natural.
    """

    # Vertex Veo API 호출
    result = client.models.generate_videos(
        model=MODEL_ID,
        prompt=prompt,
        images=[imgA_b64, imgB_b64],   # 중요: Veo는 이렇게 받아야 함
        duration_seconds=2,            # 원하는 길이
        fps=30,
    )

    # 결과 저장
    for vid in result.videos:
        with open(output_path, "wb") as f:
            f.write(vid.buffer)
        print("🎉 영상 저장 완료:", output_path)
        return output_path

    print("❌ 결과 영상 없음")
    return None
