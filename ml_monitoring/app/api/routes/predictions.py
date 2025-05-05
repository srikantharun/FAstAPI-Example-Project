from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, List, Optional

from app.db.session import get_db
from app.schemas.prediction import (
    PredictionInput, 
    PredictionResult, 
    ActualValueInput,
    HistoricalPrediction, 
    PredictionsList
)
from app.db.base import PredictionRecord
from app.services.model_service import model_service

import logging
import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
async def predict(
    input_data: PredictionInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Make prediction with ML model and log it for monitoring.
    
    Args:
        input_data: Features for prediction
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        PredictionResult: Model prediction
    """
    try:
        # Extract features
        features = input_data.features
        
        # Make prediction
        prediction = model_service.predict(features)
        
        # Log prediction in background
        background_tasks.add_task(
            model_service.save_prediction,
            db=db,
            features=features,
            prediction=prediction
        )
        
        return PredictionResult(
            prediction=prediction,
            model_version=model_service.model_version,
            timestamp=datetime.datetime.now()
        )
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-actual-value")
async def update_actual_value(
    actual_data: ActualValueInput,
    db: Session = Depends(get_db)
):
    """
    Update prediction record with actual value.
    
    Args:
        actual_data: Actual value data
        db: Database session
        
    Returns:
        Dict: Success message
    """
    try:
        # Get prediction record
        prediction_record = db.query(PredictionRecord).filter(
            PredictionRecord.id == actual_data.prediction_id
        ).first()
        
        if not prediction_record:
            raise HTTPException(status_code=404, detail="Prediction record not found")
        
        # Update actual value
        prediction_record.actual = actual_data.actual_value
        
        db.commit()
        db.refresh(prediction_record)
        
        return {"message": "Actual value updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating actual value: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions", response_model=PredictionsList)
async def get_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get historical predictions.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        PredictionsList: List of historical prediction records
    """
    try:
        # Query predictions
        predictions = db.query(PredictionRecord).order_by(
            PredictionRecord.timestamp.desc()
        ).offset(skip).limit(limit).all()
        
        # Get total count
        total = db.query(PredictionRecord).count()
        
        # Convert to response model
        result = []
        for p in predictions:
            result.append(
                HistoricalPrediction(
                    id=p.id,
                    timestamp=p.timestamp,
                    features=p.feature_values,
                    prediction=p.prediction,
                    actual=p.actual,
                    model_version=p.model_version
                )
            )
        
        return PredictionsList(predictions=result, total=total)
    except Exception as e:
        logger.error(f"Error retrieving predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))