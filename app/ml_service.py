import logging
from transformers import pipeline
from app.config import config

logger = logging.getLogger(__name__)

class SpamDetector:
    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.classifier = None
        self._load_model()

    def _load_model(self):
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                truncation=True,
                max_length=512
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(self, text: str):
        if not self.classifier:
            raise RuntimeError("Model not loaded")
        
        result = self.classifier(text)[0]
        logger.info(f"Prediction for '{text[:50]}...' -> {result}")
        
        # Маппинг меток модели (LABEL_0 = HAM, LABEL_1 = SPAM)
        label_map = {
            "LABEL_0": "HAM",
            "LABEL_1": "SPAM",
            "ham": "HAM",
            "spam": "SPAM"
        }
        
        predicted_label = label_map.get(result["label"], result["label"].upper())
        
        return {
            "result": predicted_label,
            "score": round(result["score"], 4)
        }

# Глобальный экземпляр
spam_detector = SpamDetector()
