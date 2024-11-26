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

# Function to load and validate processed CSV against the schema
def validate_processed_csv(file_path: str):
    processed_data = pd.read_csv(file_path)
    for _, row in processed_data.iterrows():
        participant_data = {
            "id": row["ID"],
            "role": row["Mentor or Mentee?"],
            "preferences": [row[f"Preference {i}"] for i in range(1, 16)],
            "industry": row["Industry"].split(";"),
            "rankings": {f"Rank {i}": row[f"Rank {i}"] for i in range(1, 8)},
        }
        # Validate each row against the schema
        ParticipantSchema(**participant_data)

# Test case
def test_processed_csv_schema():
    # Assuming processed CSV is generated as `processed_data.csv`
    # processed_csv_path = "processed_data.csv"
    processed_csv_path = "input_data.csv"  # Placeholder path
    try:
        validate_processed_csv(processed_csv_path)
        print("All rows in the processed CSV conform to the schema.")
    except ValidationError as e:
        print(f"Validation error: {e}")

# Run the test (This would typically be run using pytest)
test_processed_csv_schema()