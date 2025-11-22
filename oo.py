import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(
    project="verdant-oven-479008-q3",
    location="us-central1",
)

MODEL_NAME = "gemini-2.5-flash"  # 여기만 바꿔서 공통으로 쓰기

model = GenerativeModel(MODEL_NAME)
resp = model.generate_content("로드뷰 길찾기용 파이프라인 테스트")
print(resp.text)
