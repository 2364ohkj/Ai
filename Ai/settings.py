import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Google Service Account JSON (환경변수에서 가져옴)
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

# Imagen model versions
IMAGEN_INTERPOLATE_MODEL = "imagen-video-alpha-1"
IMAGEN_INTERPOLATE_SEQ_MODEL = "imagen-video-alpha-1"
