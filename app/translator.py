from deep_translator import GoogleTranslator
from langdetect import detect
import logging

logger = logging.getLogger(__name__)

class TextTranslator:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='en')
    
    def detect_language(self, text: str) -> str:
        try:
            lang = detect(text)
            logger.info(f"Detected language: {lang}")
            return lang
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'en'
    
    def translate_to_english(self, text: str) -> str:
        if not text or len(text.strip()) == 0:
            return text
        
        lang = self.detect_language(text)
        if lang == 'en':
            return text
        
        try:
            translated = self.translator.translate(text)
            logger.info(f"Translated from {lang} to en: {translated[:50]}...")
            return translated
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text

translator = TextTranslator()
