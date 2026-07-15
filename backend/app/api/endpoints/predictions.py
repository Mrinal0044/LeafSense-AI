import os
from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionDetailResponse, PredictionHistoryItem
from app.services.prediction_service import PredictionService, PredictionModelSingleton

router = APIRouter()

@router.post("/predict", response_model=PredictionDetailResponse)
async def predict_leaf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Diagnose a uploaded plant leaf image. Saves the scan in user history.
    """
    # 1. Validate file extension
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: JPG, JPEG, PNG, WEBP"
        )
        
    # 2. Read image content
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read uploaded file content."
        )

    # 3. Create prediction entry
    try:
        db_prediction = PredictionService.create_prediction(
            db,
            user_id=current_user.id,
            file_bytes=content,
            original_filename=file.filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model inference failed: {str(e)}"
        )
        
    # 4. Fetch additional details from metadata dictionary
    PredictionModelSingleton.load_resources()
    details = PredictionModelSingleton._disease_database.get(db_prediction.class_id, {
        "name": db_prediction.disease_name,
        "scientific_name": db_prediction.scientific_name,
        "description": "No additional details available.",
        "symptoms": "N/A",
        "causes": "N/A",
        "treatment": "N/A",
        "prevention": "N/A"
    })
    
    return {
        "class_id": db_prediction.class_id,
        "disease_name": db_prediction.disease_name,
        "scientific_name": db_prediction.scientific_name,
        "confidence": db_prediction.confidence,
        "is_healthy": db_prediction.is_healthy,
        "details": details
    }

@router.get("/history", response_model=List[PredictionHistoryItem])
def get_history(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve diagnosis scans history for the current user. Allows filtering by disease keyword.
    """
    return PredictionService.get_user_history(db, user_id=current_user.id, search_query=search)

@router.delete("/history/{prediction_id}", status_code=status.HTTP_200_OK)
def delete_history_item(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a scan entry from the user's diagnosis history and discard its file.
    """
    success = PredictionService.delete_prediction(
        db, 
        user_id=current_user.id, 
        prediction_id=prediction_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction history entry not found or unauthorized to delete."
        )
    return {"message": "Prediction history entry deleted successfully."}
