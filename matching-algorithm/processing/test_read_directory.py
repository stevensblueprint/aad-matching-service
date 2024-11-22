import pytest
from .read_directory import read_directory

def test_read_diretory():
  directory = read_directory("mentee_directory_15.csv")
  assert(len(directory) == 15), f"Expected 15 rows, but got {len(read_directory)}"

if __name__ == "__main__":
  pytest.main()