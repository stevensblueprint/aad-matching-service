from pydantic import BaseModel, ValidationError
from typing import List, Dict
import pandas as pd
import pytest


# Define the expected schema using Pydantic
class ParticipantSchema(BaseModel):
    id: int
    role: str  # "Mentor" or "Mentee"
    preferences: List[int]  # Up to 15 preferences
    industry: List[str]  # List of industries
    rankings: Dict[str, int]  # Rank 1 to Rank 7 as keys


# FIXME: On the algorithm side we may have to change in case people enter duplicate responses
def test_no_null_values():
    # Assuming processed CSV is generated as `processed_data.csv`
    processed_csv_path = "processed_data.csv"
    processed_data = pd.read_csv(processed_csv_path)

    # Check for NaN values
    assert (
        not processed_data.isnull().values.any()
    ), "There are NaN values in the processed data."

    # Check for empty strings
    assert not (
        processed_data.map(lambda x: x == "").values.any()
    ), "There are empty string values in the processed data."

    print("No NaN or empty string values found in the processed data.")


# Function to load and validate processed CSV against the schema
def validate_processed_csv(file_path: str):
    processed_data = pd.read_csv(file_path)
    for _, row in processed_data.iterrows():
        participant_data = {
            "id": row["id"],
            "role": row["Mentor or Mentee"],
            "preferences": [row[f"preference_{i}"] for i in range(1, 16)],
            "industry": row["industry"].split(";"),
            "rankings": {f"rank_{i}": row[f"rank_{i}"] for i in range(1, 7)},
        }
        # Validate each row against the schema
        ParticipantSchema(**participant_data)


# Test case
def test_processed_csv_schema():
    # Assuming processed CSV is generated as `processed_data.csv`
    processed_csv_path = "processed_data.csv"
    try:
        validate_processed_csv(processed_csv_path)
        print("All rows in the processed CSV conform to the schema.")
    except ValidationError as e:
        print(f"Validation error: {e}")


def test_int_types():
    # Assuming processed CSV is generated as `processed_data.csv`
    processed_csv_path = "processed_data.csv"
    processed_data = pd.read_csv(processed_csv_path)
    for i in range(1, 16):
        assert (
            processed_data[f"preference_{i}"].dtype == "int64"
        ), f"Column preference_{i} is not of type int"
    for i in range(1, 7):
        assert (
            processed_data[f"rank_{i}"].dtype == "int64"
        ), f"Column rank_{i} is not of type int"
    print("All preference and rank columns are of type int.")


# Run the test (This would typically be run using pytest)
test_processed_csv_schema()
