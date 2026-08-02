import json
import os
import uuid
import logging
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.prediction import PredictionHistory
from app.schemas.prediction import PredictionDetailResponse, DiseaseDetails

# Setup logger
logger = logging.getLogger("prediction_service")
logger.setLevel(logging.INFO)

# Try to import TF/OpenCV inside singleton to handle environments gracefully
try:
    # pyrefly: ignore [missing-import]
    import cv2
    import numpy as np
    import tensorflow as tf
    HAS_ML_LIBS = True
except ImportError:
    HAS_ML_LIBS = False
    logger.warning("TensorFlow or OpenCV not installed in this environment. ML predictions will run in Mock Mode.")

class PredictionModelSingleton:
    _model = None
    _class_indices = None
    _disease_database = None

    @classmethod
    def load_resources(cls):
        """
        Load Keras model and indices dictionaries once into class parameters.
        """
        import time
        if not HAS_ML_LIBS:
            # Fallback mock setup if ML libs are not present
            cls._class_indices = {str(i): f"Mock_Class_{i}" for i in range(38)}
            cls._class_indices["0"] = "Tomato___Early_blight"
            cls._class_indices["1"] = "Apple___Apple_scab"
            cls._class_indices["2"] = "Strawberry___healthy"
            cls._disease_database = {}
            return

        if cls._model is None:
            start_time = time.time()
            logger.info("Loading TensorFlow model...")
            logger.info(f"Model path: {settings.MODEL_PATH}")
            if not os.path.exists(settings.MODEL_PATH):
                raise FileNotFoundError(f"Model weights file not found at: {settings.MODEL_PATH}. Run training first.")
            cls._model = tf.keras.models.load_model(settings.MODEL_PATH)
            logger.info("TensorFlow model loaded")
            
            logger.info("Loading class_indices.json")
            with open(settings.CLASS_INDICES_PATH, "r") as f:
                cls._class_indices = json.load(f)
            logger.info("class_indices loaded")
                
            logger.info("Loading disease_info.json")
            with open(settings.DISEASE_INFO_PATH, "r") as f:
                cls._disease_database = json.load(f)
            logger.info("Disease database loaded")
            
            duration = time.time() - start_time
            logger.info(f"Prediction resources ready (took {duration:.2f} seconds)")

    @classmethod
    def predict_image(cls, image_bytes: bytes) -> dict:
        """
        Execute in-memory model inference using the cached model.
        """
        cls.load_resources()
        
        # Mock mode fallback if tensorflow is not present
        if not HAS_ML_LIBS or cls._model is None:
            # Simulate high-confidence prediction for Tomato Early Blight
            class_folder = "Tomato___Early_blight"
            details = {
                "name": "Tomato Early Blight",
                "scientific_name": "Alternaria solani",
                "description": "A common fungal disease causing circular spots with concentric rings.",
                "symptoms": "Dark target-board spots on lower leaves.",
                "causes": "Fungal spores overwintering in soil.",
                "treatment": "Copper fungicides.",
                "prevention": "Prune lower leaves, apply mulch."
            }
            return {
                "class_id": class_folder,
                "disease_name": details["name"],
                "scientific_name": details["scientific_name"],
                "confidence": 0.9412,
                "is_healthy": False,
                "details": details
            }

        # 1. Decode image bytes in memory
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image bytes. Mismatched or corrupted image file format.")
            
        # 2. Convert BGR to RGB and resize
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        
        # 3. Shape input tensor
        img_batch = np.expand_dims(img, axis=0).astype(np.float32)
        
        # 4. Predict
        predictions = cls._model.predict(img_batch, verbose=0)[0]
        predicted_idx = str(np.argmax(predictions))
        confidence = float(predictions[int(predicted_idx)])
        
        class_folder = cls._class_indices.get(predicted_idx, "Tomato___healthy")
        details = cls._disease_database.get(class_folder, {
            "name": class_folder.replace("___", " ").replace("_", " "),
            "scientific_name": "Unknown",
            "description": "N/A",
            "symptoms": "N/A",
            "causes": "N/A",
            "treatment": "N/A",
            "prevention": "N/A"
        })
        
        return {
            "class_id": class_folder,
            "disease_name": details.get("name"),
            "scientific_name": details.get("scientific_name"),
            "confidence": confidence,
            "is_healthy": "healthy" in class_folder.lower(),
            "details": details
        }

class PredictionService:
    @staticmethod
    def _resolve_and_detach(db: Session, record: PredictionHistory) -> PredictionHistory:
        """
        Detaches the record from the SQLAlchemy session to prevent temporary
        mutations (e.g. S3 pre-signed URLs) from being persisted to the database,
        and dynamically updates the image path if S3 storage is enabled.
        """
        db.expunge(record)
        if settings.USE_S3_STORAGE:
            from app.services.s3_service import S3Service
            filename = os.path.basename(record.image_path)
            record.image_path = S3Service.generate_presigned_url(filename)
        return record

    @staticmethod
    def create_prediction(
        db: Session, 
        *, 
        user_id: int, 
        file_bytes: bytes, 
        original_filename: str
    ) -> PredictionHistory:
        """
        Processes image upload, performs ML classification, and saves records.
        """
        # Generate unique image path name
        file_ext = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        relative_path = f"uploads/{unique_filename}"

        if settings.USE_S3_STORAGE:
            # Upload to S3 directly
            from app.services.s3_service import S3Service
            content_type = "image/jpeg"
            if file_ext.lower() in [".png"]:
                content_type = "image/png"
            elif file_ext.lower() in [".webp"]:
                content_type = "image/webp"
            
            success = S3Service.upload_file(file_bytes, unique_filename, content_type=content_type)
            if not success:
                logger.error("S3 upload failed, falling back to local file storage")
                # Fallback to local storage if S3 fails
                os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
                saved_file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
                with open(saved_file_path, "wb") as f:
                    f.write(file_bytes)
        else:
            # Save file to local disk
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            saved_file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            with open(saved_file_path, "wb") as f:
                f.write(file_bytes)
            
        # Run ML Classification
        prediction_result = PredictionModelSingleton.predict_image(file_bytes)
        
        db_prediction = PredictionHistory(
            user_id=user_id,
            image_path=relative_path,
            class_id=prediction_result["class_id"],
            disease_name=prediction_result["disease_name"],
            scientific_name=prediction_result["scientific_name"],
            confidence=prediction_result["confidence"],
            is_healthy=prediction_result["is_healthy"]
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction

    @staticmethod
    def get_user_history(
        db: Session, 
        *, 
        user_id: int, 
        search_query: Optional[str] = None
    ) -> List[PredictionHistory]:
        """
        Retrieve prediction listings for a user. Supports keyword query filtering.
        """
        query = db.query(PredictionHistory).filter(PredictionHistory.user_id == user_id)
        
        if search_query:
            # Case insensitive search on disease name, class name, or scientific name
            search_pattern = f"%{search_query}%"
            query = query.filter(
                (PredictionHistory.disease_name.ilike(search_pattern)) | 
                (PredictionHistory.scientific_name.ilike(search_pattern)) |
                (PredictionHistory.class_id.ilike(search_pattern))
            )
            
        records = query.order_by(PredictionHistory.prediction_date.desc()).all()
        # Resolve path urls dynamically
        return [PredictionService._resolve_and_detach(db, r) for r in records]

    @staticmethod
    def delete_prediction(
        db: Session, 
        *, 
        user_id: int, 
        prediction_id: int
    ) -> bool:
        """
        Deletes prediction from database and removes image asset from S3 or local disk.
        """
        prediction = db.query(PredictionHistory).filter(
            PredictionHistory.id == prediction_id,
            PredictionHistory.user_id == user_id
        ).first()
        
        if not prediction:
            return False
            
        # Delete from appropriate storage
        filename = os.path.basename(prediction.image_path)
        if settings.USE_S3_STORAGE:
            from app.services.s3_service import S3Service
            S3Service.delete_file(filename)
        else:
            image_absolute_path = os.path.join(
                os.path.dirname(settings.UPLOAD_DIR), 
                prediction.image_path
            )
            try:
                if os.path.exists(image_absolute_path):
                    os.remove(image_absolute_path)
            except Exception as e:
                logger.warning(f"Failed to delete physical file {image_absolute_path}: {e}")
            
        # Delete DB Record
        db.delete(prediction)
        db.commit()
        return True

    @staticmethod
    def get_dashboard_statistics(db: Session, *, user_id: int) -> dict:
        """
        Aggregate and compile dashboard metrics: counts, healthy ratios, common diseases, confidence distributions.
        """
        total = db.query(PredictionHistory).filter(PredictionHistory.user_id == user_id).count()
        
        # Healthy vs Diseased count
        healthy = db.query(PredictionHistory).filter(
            PredictionHistory.user_id == user_id,
            PredictionHistory.is_healthy == True
        ).count()
        
        diseased = total - healthy
        
        # Most Common Diseases (limited to diseased foliage only)
        common_query = db.query(
            PredictionHistory.disease_name,
            func.count(PredictionHistory.id).label("count")
        ).filter(
            PredictionHistory.user_id == user_id,
            PredictionHistory.is_healthy == False
        ).group_by(
            PredictionHistory.disease_name
        ).order_by(
            func.count(PredictionHistory.id).desc()
        ).limit(5).all()
        
        most_common = [{"disease_name": name, "count": count} for name, count in common_query]
        
        # Confidence distribution
        confidence_records = db.query(PredictionHistory.confidence).filter(
            PredictionHistory.user_id == user_id
        ).all()
        
        ranges = {
            "0-20%": 0,
            "20-40%": 0,
            "40-60%": 0,
            "60-80%": 0,
            "80-100%": 0
        }
        for (conf,) in confidence_records:
            val = conf * 100
            if val <= 20:
                ranges["0-20%"] += 1
            elif val <= 40:
                ranges["20-40%"] += 1
            elif val <= 60:
                ranges["40-60%"] += 1
            elif val <= 80:
                ranges["60-80%"] += 1
            else:
                ranges["80-100%"] += 1
                
        confidence_distribution = [
            {"range_label": label, "count": count} 
            for label, count in ranges.items()
        ]
        
        # Fetch 5 most recent predictions
        recent = db.query(PredictionHistory).filter(
            PredictionHistory.user_id == user_id
        ).order_by(
            PredictionHistory.prediction_date.desc()
        ).limit(5).all()
        
        # Resolve S3 paths for recent list
        resolved_recent = [PredictionService._resolve_and_detach(db, r) for r in recent]
        
        return {
            "total_predictions": total,
            "healthy_vs_diseased": {
                "healthy": healthy,
                "diseased": diseased
            },
            "most_common_diseases": most_common,
            "confidence_distribution": confidence_distribution,
            "recent_predictions": resolved_recent
        }

