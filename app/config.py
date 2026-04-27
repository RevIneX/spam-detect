import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@postgres:5432/spam-detect")
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "ssheroz/spam-email-classifier-roberta-r4")
    API_KEY = os.getenv("API_KEY", "")
    MAX_TEXT_LENGTH = 500


config = Config()
