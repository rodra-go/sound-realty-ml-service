from typing import List

from pydantic import BaseModel, confloat, conint


class Metadata(BaseModel):
    ml_model_version: conint(ge=1)
    sales_features: List[str]
    demographic_features: List[str]


class PredictionOutput(BaseModel):
    prediction: confloat(ge=0)
    metadata: Metadata
