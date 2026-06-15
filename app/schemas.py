from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AnalyzeResponse(BaseModel):
    result: str
    score: float


class HistoryResponse(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
