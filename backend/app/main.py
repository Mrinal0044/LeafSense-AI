import logging
import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.api import api_router
from app.database.session import engine
from app.database.base_class import Base
# Import models to ensure they are registered on the metadata for table creation
from app.models.user import User
from app.models.prediction import PredictionHistory
from app.services.prediction_service import PredictionModelSingleton

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("leafsense_api")

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for LeafSense AI Plant Health Management Platform",
    version="1.0.0"
)

# Set up CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the physical uploads directory to serve stored images statically
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include master API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    """
    Application startup sequence: creates tables and loads model into memory.
    """
    logger.info("Initializing database and metadata tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("Caching ML models and indices resources in memory...")
    try:
        PredictionModelSingleton.load_resources()
    except Exception as e:
        logger.error(f"Error loading model resources at startup: {e}")

# Global Exception Handlers for clean API reports
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on request {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A critical system error occurred. Please contact the administrator."}
    )

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring service status.
    """
    return {
        "status": "healthy",
        "service": "LeafSense AI Backend API",
        "version": "1.0.0",
        "database": "connected",
        "model_loaded": PredictionModelSingleton._model is not None
    }

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint welcome message.
    """
    return {
        "message": "Welcome to LeafSense AI API. Refer to /docs for API documentation."
    }
