"""Dataset routes for example images."""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import random
from typing import List
from pydantic import BaseModel

from src.datasets.ham10000 import HAM10000DatasetInfo

router = APIRouter()

# Initialize dataset info globally to load once
# This will be triggered on first import or request
dataset_info = HAM10000DatasetInfo()
try:
    metadata_df = dataset_info.load()
    # Cache the dataframe
    print(f"Loaded HAM10000 metadata: {len(metadata_df)} rows")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    metadata_df = pd.DataFrame()

# Class mappings for full names
CLASS_NAMES = {
    'MEL': 'Melanoma',
    'NV': 'Melanocytic Nevus',
    'BCC': 'Basal Cell Carcinoma',
    'AKIEC': 'Actinic Keratoses',
    'BKL': 'Benign Keratosis',
    'DF': 'Dermatofibroma',
    'VASC': 'Vascular Lesion'
}

class ExampleImage(BaseModel):
    id: str
    class_name: str
    name: str
    url: str

@router.get("/examples/random", response_model=List[ExampleImage])
async def get_random_examples(count: int = 8):
    """Get random example images from the dataset."""
    if metadata_df.empty:
        raise HTTPException(status_code=500, detail="Dataset not available")
    
    # Sample random rows
    sample_df = metadata_df.sample(n=min(count, len(metadata_df)))
    
    examples = []
    for _, row in sample_df.iterrows():
        image_id = row['image_id']
        dx = row['dx']
        # The frontend will use this URL to fetch the actual image file
        url = f"/api/examples/image/{image_id}"
        
        examples.append(ExampleImage(
            id=image_id,
            class_name=dx.upper(),
            name=CLASS_NAMES.get(dx.upper(), dx.upper()),
            url=url
        ))
        
    return examples

@router.get("/examples/image/{image_id}")
async def get_example_image(image_id: str):
    """Serve the actual image file."""
    if metadata_df.empty:
        raise HTTPException(status_code=500, detail="Dataset not available")
        
    # Find the image path in the dataframe
    matches = metadata_df[metadata_df['image_id'] == image_id]
    if matches.empty:
        raise HTTPException(status_code=404, detail="Image not found")
        
    image_path = matches.iloc[0]['image_path']
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image file not found on disk")
        
    return FileResponse(image_path, media_type="image/jpeg")
