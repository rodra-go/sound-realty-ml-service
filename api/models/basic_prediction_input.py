from pydantic import BaseModel, confloat, conint, constr, validator


class BasicPredictionInput(BaseModel):
    bedrooms: conint(ge=0)
    bathrooms: confloat(ge=0)
    sqft_living: conint(ge=1)
    sqft_lot: conint(ge=1)
    floors: confloat(ge=1)
    sqft_above: conint(ge=0)
    sqft_basement: conint(ge=0)
    zipcode: constr(min_length=5, max_length=5)

    @validator("zipcode")
    def validate_zipcode(cls, value):
        if not value.isdigit():
            raise ValueError("Zipcode must be a numeric string")
        zipcode_num = int(value)
        if not (501 <= zipcode_num <= 99950):
            raise ValueError("Zipcode must be in the range of 00501 to 99950")
        return value
