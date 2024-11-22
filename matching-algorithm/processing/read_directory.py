import pandas as pd

def read_directory(filepath):
  """filepath: the directory path to csv"""
  df = pd.read_csv(filepath)
  directory = {}

  for index, row in df.iterrows():
    directory[row.iloc(0)] = row

  return directory