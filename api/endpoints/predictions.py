import json
import logging
import os
from functools import lru_cache
from typing import Union

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from api.models.basic_prediction_input import BasicPredictionInput
from api.models.prediction_input import PredictionInput
from api.models.prediction_output import PredictionOutput

# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Set the desired logging level
logger = logging.getLogger(__name__)

# Load Environment Variables
MODEL_VERSION = os.environ.get("MODEL_VERSION", "1")
MODEL_DIR_PATH = os.environ.get("MODEL_DIR_PATH", "models")
DEMOGRAPHIC_DATA_PATH = os.environ.get(
    "DEMOGRAPHIC_DATA_PATH", "data/zipcode_demographics.csv"
)

# Configure model variables
model_path = f"./models/versions/{MODEL_VERSION}/model.pkl"
load_model_feature_list_path = f"./models/versions/{MODEL_VERSION}/model_features.json"

# Instantiate router
router = APIRouter()


# Load demographic data
@lru_cache(maxsize=None)
def load_demographic_data():
    try:
        demographic_data = pd.read_csv(DEMOGRAPHIC_DATA_PATH)
        demographic_data.set_index("zipcode", inplace=True)
        return demographic_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading demographic data: {str(e)}"
        )


# Load model
@lru_cache(maxsize=None)
def load_model():
    try:
        # Load the model
        return joblib.load(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


# Load model features
@lru_cache(maxsize=None)
def load_model_feature_list():
    try:
        with open(load_model_feature_list_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading model features: {str(e)}"
        )


def get_features(input_data, demographic_data, feature_list):
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

    return features[feature_list]


async def predict_price(
    input_data: Union[PredictionInput, BasicPredictionInput]
) -> PredictionOutput:
    try:
        logger.info("Starting prediction process...")

        # Load demographic data
        demographic_data = load_demographic_data()

        # Load model and model feature list
        model = load_model()
        feature_list = load_model_feature_list()

        # Get model features
        features = get_features(input_data, demographic_data, feature_list)

        # Make prediction
        prediction = model.predict(features)

        # Prepare metadata
        metadata = {
            "model_version": int(MODEL_VERSION),
            "sales_features": list(input_data.__fields__),
            "demographic_features": list(demographic_data.columns),
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


@router.post(
    "/predict_basic", response_model=PredictionOutput, tags=["Basic Prediction"]
)
async def predict_basic(input_data: BasicPredictionInput):
    return await predict_price(input_data)
