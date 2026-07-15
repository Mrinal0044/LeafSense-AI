from typing import List
from pydantic import BaseModel
from app.schemas.prediction import PredictionHistoryItem

class HealthyVsDiseased(BaseModel):
    healthy: int
    diseased: int

class MostCommonDisease(BaseModel):
    disease_name: str
    count: int

class ConfidenceRange(BaseModel):
    range_label: str # e.g. "0-20%", "20-40%", etc.
    count: int

class DashboardStatsResponse(BaseModel):
    total_predictions: int
    healthy_vs_diseased: HealthyVsDiseased
    most_common_diseases: List[MostCommonDisease]
    confidence_distribution: List[ConfidenceRange]
    recent_predictions: List[PredictionHistoryItem]
