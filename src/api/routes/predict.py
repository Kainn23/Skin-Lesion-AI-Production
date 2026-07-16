"""Prediction routes."""

import io
from fastapi import APIRouter, File, Request, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError

import numpy as np

from src.inference.preprocess import preprocess_image
from src.inference.predictor import Predictor
from src.api.schemas import PredictionResponse, GradCAMResponse, ErrorResponse
from src.analysis.abcde import analyze_abcde

router = APIRouter(responses={400: {"model": ErrorResponse}})


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), request: Request = None) -> PredictionResponse:
    contents = await file.read()
    
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
        
    tensor = preprocess_image(image)

    predictor: Predictor = request.app.state.predictor
    prediction_dict = predictor.predict(tensor)
    
    # Run ABCDE analysis
    try:
        img_array = np.array(image)
        abcde_results = analyze_abcde(img_array)
        prediction_dict["abcde"] = abcde_results
    except Exception as e:
        print(f"ABCDE analysis failed: {e}")
        prediction_dict["abcde"] = None
    
    return PredictionResponse(**prediction_dict)


@router.post("/gradcam", response_model=GradCAMResponse)
async def gradcam(file: UploadFile = File(...), request: Request = None) -> GradCAMResponse:
    contents = await file.read()
    
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
        
    tensor = preprocess_image(image)

    predictor: Predictor = request.app.state.predictor
    prediction_dict = predictor.predict(tensor)
    gradcam_path = predictor.generate_gradcam(tensor, image)

    return GradCAMResponse(
        prediction=prediction_dict["prediction"],
        confidence=prediction_dict["confidence"],
        gradcam_path=gradcam_path,
    )
