import os

PERPLEXITY_API_KEY = "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"
PERPLEXITY_MODEL = "sonar-pro"
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

UPLOAD_DIR = "data/uploads"
DATABASE_PATH = "data/knowledge_base.db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

SUPPORTED_TEXT_FORMATS = ['.pdf', '.docx', '.pptx', '.txt', '.md']
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a']
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv']
