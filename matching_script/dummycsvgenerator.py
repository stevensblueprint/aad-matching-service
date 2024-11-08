import numpy as np
import pandas as pd
import random

industries = [
    "Mining", "Construction", "Information Technology", "Pharmaceuticals", "Real Estate", "Hospitality", 
    "Energy", "Automotive", "Agriculture", "Telecommunications", "Transportation and Logistics", 
    "Manufacturing", "Biotechnology", "Consumer Goods"
]

class RandomGenerator:
  def __init__(self, num_people, num_preferences, num_questions):
    self.num_people = num_people
    self.num_preferences = num_preferences
    self.num_questions = num_questions
    self.df = pd.DataFrame()
  
  def create(self):
    ids = [i for i in range(0, self.num_people)]
    ids.extend(ids)
    self.df['ID'] = ids
    self.df.loc[:self.num_people, 'Mentor or Mentee?'] = "Mentor"
    self.df.loc[self.num_people:, 'Mentor or Mentee?'] = "Mentee"
    
    for i in range(0, self.num_people * 2):
      self.df.loc[i, [f'Preference {j+1}' for j in range(self.num_preferences)]] = random.sample(range(0, self.num_people), self.num_preferences)
      specific_industries = random.sample(industries, random.randint(1,5))
      self.df.loc[i, 'Industry'] = ";".join(specific_industries)
      self.df.loc[i, [f'Rank {j+1}' for j in range(self.num_questions)]] = random.sample(range(1, 11), self.num_questions)
    
    for i in range(self.num_preferences):
      self.df[f'Preference {i+1}'] = self.df[f'Preference {i+1}'].astype(int)
    
    for i in range(self.num_questions):
      self.df[f'Rank {i+1}'] = self.df[f'Rank {i+1}'].astype(int)
  
  def export(self):
    self.df.to_csv('input_data.csv', index=False)

rg = RandomGenerator(200,15,7)
rg.create()
rg.export()