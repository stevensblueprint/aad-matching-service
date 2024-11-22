import pytest
from .generate_matching_responses import generate_responses

def test_generate_matching_responses_shape():
    df = generate_responses("mentee_directory", "mentor_directory")
    assert df.shape[1] == 59, f"Expected 59 columns, but got {df.shape[1]}"

if __name__ == "__main__":
    pytest.main()