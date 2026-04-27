import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
from app.config import config

logger = logging.getLogger(__name__)


class SpamDetector:
    def __init__(self):
        self.model_name_or_path = config.MODEL_NAME
        self.base_model_name = "FacebookAI/roberta-base"
        self.model_name = self.model_name_or_path
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        logger.info(f"Loading base model: {self.base_model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        logger.info("Loading base model for sequence classification")
        base_model = AutoModelForSequenceClassification.from_pretrained(
            self.base_model_name,
            num_labels=2,
            problem_type="single_label_classification"
        )

        logger.info(f"Loading LoRA adapter: {self.model_name_or_path}")
        self.model = PeftModel.from_pretrained(
            base_model, self.model_name_or_path)
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"Model loaded successfully on {self.device}")

    def predict(self, text: str):
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][prediction].item()

        label = "SPAM" if prediction == 1 else "HAM"
        logger.info(
            f"Prediction for '{text[:50]}...' -> {label} (confidence: {confidence:.4f})")

        return {
            "result": label,
            "score": round(confidence, 4)
        }


_spam_detector = None


def get_spam_detector():
    global _spam_detector
    if _spam_detector is None:
        _spam_detector = SpamDetector()
    return _spam_detector
