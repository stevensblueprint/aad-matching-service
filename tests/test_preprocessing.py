import pytest
from pydantic import BaseModel, ValidationError
from typing import List, Dict
from pathlib import Path
import pandas as pd

from src.preprocessing import process_form_data

data_dir = Path(__file__).resolve().parent.parent / "data"


# Define the expected schema using Pydantic
class ParticipantSchema(BaseModel):
    id: int
    role: str  # "Mentor" or "Mentee"
    preferences: List[int]  # Up to 15 preferences
    industry: List[str]  # List of industries
    rankings: Dict[str, int]  # Rank 1 to Rank 7 as keys


@pytest.fixture
def generate_processed_data():
    raw_input_path = data_dir / "raw_inputs/matching_responses.csv"
    processed_data = process_form_data(raw_input_path)
    return processed_data


def test_no_null_values(generate_processed_data: pd.DataFrame):
    # generate_processed_data is a fixture that returns the processed data as a DataFrame
    processed_data = generate_processed_data

    # Check for NaN values
    assert (
        not processed_data.isnull().values.any()
    ), "There are NaN values in the processed data."

    # Check for empty strings
    assert not (
        processed_data.map(lambda x: x == "").values.any()
    ), "There are empty string values in the processed data."

    print("No NaN or empty string values found in the processed data.")


def validate_processed_csv(processed_data: pd.DataFrame):
    """Helper function to validate the processed CSV against the schema."""
    for _, row in processed_data.iterrows():
        participant_data = {
            "id": row["id"],
            "role": row["mentor_or_mentee"],
            "preferences": [row[f"preference_{i}"] for i in range(1, 16)],
            "industry": row["industry"].split(";"),
            "rankings": {f"rank_{i}": row[f"rank_{i}"] for i in range(1, 7)},
        }
        # Validate each row against the schema
        ParticipantSchema(**participant_data)


def test_processed_csv_schema(generate_processed_data: pd.DataFrame):
    processed_data = generate_processed_data
    try:
        validate_processed_csv(processed_data)
        print("All rows in the processed DataFrame conform to the schema.")
    except ValidationError as e:
        print(f"Validation error: {e}")


def test_int_types(generate_processed_data: pd.DataFrame):
    processed_data = generate_processed_data
    for i in range(1, 16):
        assert (
            processed_data[f"preference_{i}"].dtype == "int64"
        ), f"Column preference_{i} is not of type int"
    for i in range(1, 7):
        assert (
            processed_data[f"rank_{i}"].dtype == "int64"
        ), f"Column rank_{i} is not of type int"
    print("All preference and rank columns are of type int.")


if __name__ == "__main__":
    pytest.main()
