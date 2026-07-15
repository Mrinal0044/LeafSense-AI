from fastapi import APIRouter
from app.api.endpoints import auth, predictions, dashboard, profile

api_router = APIRouter()

# Register sub-routers with clean prefix groups
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
