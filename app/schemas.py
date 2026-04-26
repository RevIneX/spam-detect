from pydantic import BaseModel, Field
from datetime import datetime

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

class AnalyzeResponse(BaseModel):
    result: str
    score: float

class HistoryResponse(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

class HealthResponse(BaseModel):
    status: str
