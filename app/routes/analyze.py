from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.ml_service import get_spam_detector
from app.models import RequestHistory
from app.db import get_db
from app.config import config
from app.translator import translator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    original_text = request.text.strip()
    
    if not original_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(original_text) > config.MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text too long. Max {config.MAX_TEXT_LENGTH} characters")
    
    try:
        # Определяем язык и при необходимости переводим на английский
        text_for_model = translator.translate_to_english(original_text)
        
        spam_detector = get_spam_detector()
        result = spam_detector.predict(text_for_model)
        
        # Сохраняем в БД исходный текст (оригинал)
        history = RequestHistory(
            input_text=original_text,
            result_text=f"{result['result']}:{result['score']}",
            model_name=spam_detector.model_name
        )
        db.add(history)
        db.commit()
        
        return AnalyzeResponse(result=result["result"], score=result["score"])
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")
