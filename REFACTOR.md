# Modified Gale-Shapley Algorithm: 5-Step Outline

## 1. Structuring the Code
### a. Separation of Concerns
- **Form Processing Layer:** Processes raw form data into a normalized schema.
- **Algorithm Input Layer:** Maps processed data to the input required by the Gale-Shapley algorithm.
- **Algorithm Execution Layer:** Runs the Gale-Shapley matching process using the formatted inputs.

### b. Modular Components
- **Form Schema Configuration:**
  - Use a `config.py` file or JSON configuration to define expected form fields and their mappings.
  - Example:
    ```python
    FORM_SCHEMA = {
        "preferences": "top_preferences",
        "industry": "preferred_industry",
        "gender": "preferred_gender",
        "ranked_questions": ["q1", "q2", "q3"]
    }
    ```

- **Preprocessing Functions:**
  - Write modular preprocessing functions for each field or group of fields.
  - Example:
    ```python
    def preprocess_preferences(raw_preferences):
        # Clean, validate, and format preferences
        return processed_preferences

    def preprocess_similarity_scores(data, form_fields):
        # Generate similarity scores based on input fields
        return similarity_scores
    ```

- **Algorithm Inputs Mapping:**
  - Create a mapper function that aligns preprocessed data to the Gale-Shapley algorithm's expected inputs.
  - Example:
    ```python
    def map_to_algorithm_input(preprocessed_data):
        # Map cleaned data to algorithm input format
        return mentors, mentees
    ```

---

## 2. Directory Structure
```
project/
│
├── src/
│   ├── config/
│   │   └── config.py         # Form schema and configurations
│   ├── data/
│   │   └── form_data.csv     # Raw data files
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── form_processor.py # Form preprocessing logic
│   │   └── similarity.py     # Similarity score calculation
│   ├── algorithm/
│   │   ├── __init__.py
│   │   ├── gale_shapley.py   # Core Gale-Shapley algorithm
│   │   └── input_mapper.py   # Mapping logic for algorithm inputs
│   └── main.py               # Orchestrates the pipeline
│
├── tests/
│   ├── test_preprocessing.py # Tests for form_processor and similarity
│   ├── test_algorithm.py     # Tests for gale_shapley algorithm
│   └── test_integration.py   # End-to-end tests
│
└── requirements.txt          # Dependencies
```

---

## 3. Matching Schema Between Preprocessing and Algorithm Input
### a. Define an Interface Contract
- Use Python type hints or a schema validator like `pydantic` to define the structure of algorithm inputs.
- Example with `pydantic`:
    ```python
    from pydantic import BaseModel
    from typing import List, Dict

    class Participant(BaseModel):
        id: int
        preferences: List[int]
        similarity_scores: Dict[int, float]

    class AlgorithmInput(BaseModel):
        mentors: List[Participant]
        mentees: List[Participant]
    ```

- Validate the preprocessed data before passing it to the algorithm.

### b. Preprocessing Module
- Ensure functions in the preprocessing module output data matching the defined `Participant` schema.
- Example:
    ```python
    def preprocess_data(raw_data):
        # Normalize and process raw data
        return [Participant(**data) for data in normalized_data]
    ```

---

## 4. Directory and Tests
### a. Unit Tests
- Test each preprocessing function with edge cases (e.g., missing preferences, invalid data).
- Example:
    ```python
    def test_preprocess_preferences():
        raw = {"preferences": "1,2,3"}
        expected = [1, 2, 3]
        assert preprocess_preferences(raw) == expected
    ```

### b. Integration Tests
- Test the full pipeline: form data -> preprocessing -> Gale-Shapley inputs -> matching results.
- Example:
    ```python
    def test_integration_pipeline():
        raw_data = load_test_data()
        preprocessed = preprocess_data(raw_data)
        mentors, mentees = map_to_algorithm_input(preprocessed)
        matches = gale_shapley(mentors, mentees)
        assert validate_matches(matches)
    ```

### c. Mock Data for Testing
- Store mock mentor/mentee data in a `tests/data/` directory for repeatable tests.

---

## 5. Scalability Tips
- **Config-Driven Development:** Store all dynamic mappings (e.g., form fields, weights for similarity scores) in `config.py` or JSON files.
- **Extendability:** Abstract similarity scoring logic into plugins, so you can easily add new scoring methods.
- **CI/CD Integration:** Use GitHub Actions or another CI/CD tool to automate test runs on every push.
