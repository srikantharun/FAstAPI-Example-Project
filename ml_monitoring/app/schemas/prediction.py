from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union, Any
import datetime

class PredictionInput(BaseModel):
    """
    Schema for prediction input data.
    """
    features: Dict[str, Union[float, int, str]] = Field(
        ..., 
        description="Dictionary of feature names and values"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {
                    "feature1": 1.5,
                    "feature2": 2.0,
                    "feature3": 3.0
                }
            }
        }

class PredictionResult(BaseModel):
    """
    Schema for prediction result.
    """
    prediction: float
    model_version: str
    timestamp: datetime.datetime

class ActualValueInput(BaseModel):
    """
    Schema for submitting actual values for past predictions.
    """
    prediction_id: int
    actual_value: float

class HistoricalPrediction(BaseModel):
    """
    Schema for historical prediction record.
    """
    id: int
    timestamp: datetime.datetime
    features: Dict[str, Any]
    prediction: float
    actual: Optional[float] = None
    model_version: str
    
    class Config:
        orm_mode = True

class PredictionsList(BaseModel):
    """
    Schema for list of predictions.
    """
    predictions: List[HistoricalPrediction]
    total: int