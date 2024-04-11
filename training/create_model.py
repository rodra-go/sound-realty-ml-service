import json
import os
import pathlib
import pickle
from typing import List, Tuple
import yaml

import pandas
from sklearn import model_selection, neighbors, pipeline, preprocessing

SALES_PATH = "data/kc_house_data.csv"  # path to CSV with home sale data
DEMOGRAPHICS_PATH = "data/zipcode_demographics.csv"  # path to CSV with demographics
# List of columns (subset) that will be taken from home sale data
SALES_COLUMN_SELECTION = [
    "price",
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "sqft_above",
    "sqft_basement",
    "zipcode",
]
OUTPUT_DIR = "models/versions"  # Directory where output artifacts will be saved
WORKFLOW_FILE_PATH = './.github/workflows/ci-cd-pipeline.yml'


def load_data(
    sales_path: str, demographics_path: str, sales_column_selection: List[str]
) -> Tuple[pandas.DataFrame, pandas.Series]:
    """Load the target and feature data by merging sales and demographics.

    Args:
        sales_path: path to CSV file with home sale data
        demographics_path: path to CSV file with home sale data
        sales_column_selection: list of columns from sales data to be used as
            features

    Returns:
        Tuple containg with two elements: a DataFrame and a Series of the same
        length.  The DataFrame contains features for machine learning, the
        series contains the target variable (home sale price).

    """
    data = pandas.read_csv(
        sales_path, usecols=sales_column_selection, dtype={"zipcode": str}
    )
    demographics = pandas.read_csv(demographics_path, dtype={"zipcode": str})

    merged_data = data.merge(demographics, how="left", on="zipcode").drop(
        columns="zipcode"
    )
    # Remove the target variable from the dataframe, features will remain
    y = merged_data.pop("price")
    x = merged_data

    return x, y


def find_latest_version(dir_path):
    """Finds the latest model version given the model dir path.

    Args:
        dir_path: path to the directory where models are saved

    Returns:
        An integer representing the latest version available
        or None if inexistent

    """
    # List all items in the given directory
    items = os.listdir(dir_path)

    # Filter out items that are not directories or whose names cannot be converted to integers
    dir_names_as_ints = []
    for item in items:
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            try:
                dir_names_as_ints.append(int(item))
            except ValueError:
                # Item name is not an integer, ignore this item
                continue

    # Find the maximum integer value among the directory names
    if dir_names_as_ints:
        return max(dir_names_as_ints)
    else:
        return None  # No directories with integer names


def update_cicd_variables(model_version):
    # # Read the current content of the file
    # with open(WORKFLOW_FILE_PATH, 'r') as file:
    #     data = yaml.safe_load(file)
    #
    # # Update the MODEL_VERSION environment variable
    # data['env']['MODEL_VERSION'] = str(model_version)
    #
    # # Write the modified content back to the file
    # with open(WORKFLOW_FILE_PATH, 'w') as file:
    #     yaml.safe_dump(data, file, sort_keys=False)
    with open(WORKFLOW_FILE_PATH, 'r') as file:
        lines = file.readlines()

    # Modify the MODEL_VERSION environment variable
    with open(WORKFLOW_FILE_PATH, 'w') as file:
        for line in lines:
            if line.strip().startswith('MODEL_VERSION:'):
                file.write(f'  MODEL_VERSION: \'{model_version}\'\n')  # Adjust the indentation if necessary
            else:
                file.write(line)


def main():
    """Load data, train model, and export artifacts."""
    x, y = load_data(SALES_PATH, DEMOGRAPHICS_PATH, SALES_COLUMN_SELECTION)
    x_train, _x_test, y_train, _y_test = model_selection.train_test_split(
        x, y, random_state=42
    )

    model = pipeline.make_pipeline(
        preprocessing.RobustScaler(), neighbors.KNeighborsRegressor()
    ).fit(x_train, y_train)

    model_version = find_latest_version(OUTPUT_DIR)
    if model_version is None:
        model_version = '1'
    else:
        model_version += 1

    update_cicd_variables(model_version)

    output_dir = pathlib.Path(OUTPUT_DIR / pathlib.Path(str(model_version)))
    output_dir.mkdir(exist_ok=True)

    # Output model artifacts: pickled model and JSON list of features
    pickle.dump(model, open(output_dir / "model.pkl", "wb"))
    json.dump(list(x_train.columns), open(output_dir / "model_features.json", "w"))


if __name__ == "__main__":
    main()
