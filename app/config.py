import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/spam-detect")
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "mrm8488/bert-tiny-finetuned-sms-spam-detection")
    API_KEY = os.getenv("API_KEY", "")
    MAX_TEXT_LENGTH = 500


config = Config()
