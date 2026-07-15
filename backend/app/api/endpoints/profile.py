from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.prediction import PredictionHistory

router = APIRouter()

@router.get("/me")
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details, upload count, and basic prediction statistics for the current user.
    """
    upload_count = db.query(PredictionHistory).filter(
        PredictionHistory.user_id == current_user.id
    ).count()
    
    healthy_count = db.query(PredictionHistory).filter(
        PredictionHistory.user_id == current_user.id,
        PredictionHistory.is_healthy == True
    ).count()
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "upload_count": upload_count,
        "statistics": {
            "healthy_scans": healthy_count,
            "diseased_scans": upload_count - healthy_count
        }
    }
