import pandas as pd

def read_directory(filepath):
  """
  filepath: the directory path to csv
  returns: a dictionary where the key is the KIN ID and the value is a pandas series
  """
  df = pd.read_csv(filepath)
  directory = {}

  for index, row in df.iterrows():
    directory[row["KIN ID"]] = row.drop("KIN ID")

  return directory

if __name__ == "__main__":
  mentee_directory = read_directory("mentee_directory_15.csv")
  mentor_directory = read_directory("mentor_directory_15.csv")
  for mentee in mentee_directory:
    print(mentee)