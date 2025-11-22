import os

# ★ 키 경로를 절대경로로 정확히 지정 ★
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "/Users/wangdaehyeon/Desktop/hack_ai/keys/mykey.json"

from google.cloud import aiplatform_v1
from google.cloud.aiplatform_v1.services.prediction_service import PredictionServiceClient
import base64


def imagen_interpolate(image1_path, image2_path, output_path):
    client = PredictionServiceClient()

    with open(image1_path, "rb") as f:
        img1 = base64.b64encode(f.read()).decode("utf-8")

    with open(image2_path, "rb") as f:
        img2 = base64.b64encode(f.read()).decode("utf-8")

    endpoint = (
        "projects/<PROJECT-ID>/locations/us-central1/publishers/google/models/imagen-3.0-fast-generate-001"
    )

    payload = {
        "prompt": {
            "text": "A smooth temporal interpolation between two street-view frames"
        },
        "image1": img1,
        "image2": img2,
    }

    response = client.predict(
        endpoint=endpoint,
        instances=[payload]
    )

    img_bytes = base64.b64decode(response.predictions[0]["bytesBase64"])
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    print("🟢 이미지 보간 완료:", output_path)
