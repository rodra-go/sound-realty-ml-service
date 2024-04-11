from pydantic import ValidationError
from pytest import raises

from api.models.prediction_input import PredictionInput
from api.models.prediction_output import PredictionOutput


def test_prediction_input_validation_valid_data():
    """Test the PredictionInput model with both valid and invalid data."""
    # Valid input
    try:
        PredictionInput(
            bedrooms=3,
            bathrooms=2,
            sqft_living=1000,
            sqft_lot=1000,
            floors=1,
            waterfront=0,
            view=0,
            condition=3,
            grade=7,
            sqft_above=1000,
            sqft_basement=0,
            yr_built=1990,
            yr_renovated=0,
            zipcode="98102",
            lat=47.6097,
            long=-122.3331,
            sqft_living15=1340,
            sqft_lot15=7650,
        )
    except ValidationError:
        assert False, "PredictionInput model failed to validate correct data."


def test_prediction_input_validation_invalid_zipcode():
    """Test the PredictionInput model with invalid zipcodes to
    verify specific error messages."""

    invalid_zipcodes = [
        ("00500", "Zipcode must be in the range of 00501 to 99950"),
        ("99951", "Zipcode must be in the range of 00501 to 99950"),
        (501, "Input should be a valid string"),
        (99950, "Input should be a valid string"),
    ]

    for zipcode, expected_msg in invalid_zipcodes:
        with raises(ValidationError) as exc_info:
            PredictionInput(zipcode=zipcode)

        # Check if any of the errors contains the expected message
        assert any(expected_msg in str(err) for err in exc_info.value.errors()), (
            f"Expected error message '{expected_msg}' "
            f"not found for zipcode '{zipcode}'"
        )


def test_prediction_output_validation():
    """Ensure the PredictionOutput model works as expected."""
    try:
        PredictionOutput(
            prediction=350000.0,
            metadata={
                "ml_model_version": 1,
                "sales_features": ["feature1", "feature2"],
                "demographic_features": ["featureA", "featureB"],
            },
        )
    except ValidationError:
        assert False, "PredictionOutput model failed to validate correct data."
