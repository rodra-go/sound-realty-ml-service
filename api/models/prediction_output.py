from pydantic import BaseModel, confloat


class PredictionOutput(BaseModel):
    prediction: confloat(ge=0)
    metadata: dict
