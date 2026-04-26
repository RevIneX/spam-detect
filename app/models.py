from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db import Base

class RequestHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    result_text = Column(Text, nullable=False)
    model_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
