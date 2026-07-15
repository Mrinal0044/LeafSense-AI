from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardStatsResponse
from app.services.prediction_service import PredictionService

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve aggregated diagnostic stats for the current user's dashboard charts.
    """
    stats = PredictionService.get_dashboard_statistics(db, user_id=current_user.id)
    return stats
