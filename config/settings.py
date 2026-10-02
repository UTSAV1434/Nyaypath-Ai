import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
APP_NAME = "NyayaPath"
SUPPORTED_SCHEME_IDS = ["scheme_1", "scheme_2"]
MAX_UPLOAD_SIZE_MB = 5
