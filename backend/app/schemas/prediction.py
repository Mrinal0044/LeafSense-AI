from datetime import datetime
from pydantic import BaseModel

class DiseaseDetails(BaseModel):
    description: str
    symptoms: str
    causes: str
    treatment: str
    prevention: str

class PredictionDetailResponse(BaseModel):
    class_id: str
    disease_name: str
    scientific_name: str
    confidence: float
    is_healthy: bool
    details: DiseaseDetails

class PredictionHistoryItem(BaseModel):
    id: int
    class_id: str
    disease_name: str
    scientific_name: str
    confidence: float
    is_healthy: bool
    image_path: str
    prediction_date: datetime

    class Config:
        from_attributes = True
