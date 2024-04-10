import json
import logging
import os
from typing import Union
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from api.models.prediction_input import PredictionInput
from api.models.prediction_output import PredictionOutput
from api.models.basic_prediction_input import BasicPredictionInput

# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Set the desired logging level
logger = logging.getLogger(__name__)

# Load Environment Variables
MODEL_VERSION = os.environ.get("MODEL_VERSION", 1)
model_path = f"./models/v{MODEL_VERSION}/model.pkl"
model_features_path = f"./models/v{MODEL_VERSION}/model_features.json"

# Instantiate router
router = APIRouter()


# Load demographic data
@lru_cache(maxsize=None)
def load_demographic_data():
    try:
        demographic_data = pd.read_csv("./data/zipcode_demographics.csv")
        demographic_data.set_index("zipcode", inplace=True)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading demographic data: {str(e)}"
        )
    return demographic_data


# Load model
@lru_cache(maxsize=None)
def load_model():
    try:
        # Load the model
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


# Load model features
@lru_cache(maxsize=None)
def load_model_features():
    try:
        with open(model_features_path, "r") as f:
            model_features = json.load(f)
        return model_features
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading model features: {str(e)}"
        )


async def predict_price(input_data: Union[PredictionInput, BasicPredictionInput]) -> PredictionOutput:
    try:
        logger.info("Starting prediction process...")

        # Load demographic data
        demographic_data = load_demographic_data()

        # Load model and model features
        model = load_model()
        model_features = load_model_features()

        # Add demographic data to the input
        features = dict(input_data)
        try:
            demographic_features = dict(demographic_data.loc[int(input_data.zipcode)])
        except KeyError:
            logger.error(
                f"No demographic information found for zipcode {input_data.zipcode}"
            )
            raise KeyError(
                f"There is no demographic information "
                f"for the zipcode {input_data.zipcode}."
            )

        features.update(demographic_features)
        features = pd.Series(features).to_frame().T

        # Make prediction
        prediction = model.predict(features[model_features])

        # Prepare metadata
        metadata = {
            "model_version": f"v{MODEL_VERSION}",
            "features_used": list(features.keys()),
        }

        logger.info("Prediction process completed successfully!")
        return PredictionOutput(prediction=prediction, metadata=metadata)
    except Exception as e:
        logger.exception(f"Error making prediction: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error making prediction: {str(e)}"
        )


@router.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict(input_data: PredictionInput):
    return await predict_price(input_data)


@router.post("/predict_basic", response_model=PredictionOutput, tags=["Basic Prediction"])
async def predict(input_data: BasicPredictionInput):
    return await predict_price(input_data)
