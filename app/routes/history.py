from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import RequestHistory
from app.schemas import HistoryResponse
from app.db import get_db

router = APIRouter()

@router.get("/history")
def get_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    items = db.query(RequestHistory).order_by(desc(RequestHistory.created_at)).offset(offset).limit(limit).all()
    return [HistoryResponse.from_orm(item) for item in items]

@router.get("/history/{history_id}")
def get_history_item(history_id: int, db: Session = Depends(get_db)):
    item = db.query(RequestHistory).filter(RequestHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="History entry not found")
    return HistoryResponse.from_orm(item)
