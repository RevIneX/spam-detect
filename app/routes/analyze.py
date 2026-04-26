from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.ml_service import spam_detector
from app.models import RequestHistory
from app.db import get_db
from app.config import config
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    text = request.text.strip()
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(text) > config.MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text too long. Max {config.MAX_TEXT_LENGTH} characters")
    
    try:
        result = spam_detector.predict(text)
        
        history = RequestHistory(
            input_text=text,
            result_text=f"{result['result']}:{result['score']}",
            model_name=spam_detector.model_name
        )
        db.add(history)
        db.commit()
        
        return AnalyzeResponse(result=result["result"], score=result["score"])
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")
