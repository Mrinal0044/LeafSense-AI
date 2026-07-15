from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class PredictionHistory(Base):
    # Overwrite tablename if necessary, but base class converts this to prediction_history
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    image_path = Column(String(255), nullable=False)
    class_id = Column(String(100), nullable=False) # e.g. Tomato___Early_blight
    disease_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    is_healthy = Column(Boolean, default=False, nullable=False)
    
    prediction_date = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # Establish parent-child relationship
    user = relationship("User", back_populates="predictions")
