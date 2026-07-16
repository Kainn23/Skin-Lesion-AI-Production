from typing import List
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the API")


class PredictionClass(BaseModel):
    class_name: str = Field(..., alias="class", description="The name of the predicted class")
    confidence: float = Field(..., description="The confidence score of the prediction")


class ABCDEAnalysis(BaseModel):
    asymmetry: int = Field(..., description="Asymmetry score (0-100)")
    border_irregularity: int = Field(..., description="Border irregularity score (0-100)")
    color_variation: int = Field(..., description="Color variation score (0-100)")
    diameter: int = Field(..., description="Diameter score (0-100)")
    evolution: int | None = Field(None, description="Evolution score (None if not available)")


class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="The top predicted class")
    confidence: float = Field(..., description="The confidence score of the top prediction")
    top3: List[PredictionClass] = Field(..., description="The top 3 predictions")
    abcde: ABCDEAnalysis | None = Field(None, description="ABCDE analysis metrics")


class GradCAMResponse(BaseModel):
    prediction: str = Field(..., description="The top predicted class")
    confidence: float = Field(..., description="The confidence score of the top prediction")
    gradcam_path: str = Field(..., description="Path to the generated Grad-CAM visualization")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error details")
