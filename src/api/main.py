"""FastAPI application entrypoint."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.inference.predictor import Predictor
from src.api.routes import health, predict, dataset

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.predictor = Predictor()
    yield

app = FastAPI(title="Skin Lesion API", version="0.1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(dataset.router)

if not os.path.exists("outputs"):
    os.makedirs("outputs")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
