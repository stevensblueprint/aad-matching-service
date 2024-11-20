import numpy as np
import pandas as pd
import random

industries = [
    "Mining", "Construction", "Information Technology", "Pharmaceuticals", "Real Estate", "Hospitality", 
    "Energy", "Automotive", "Agriculture", "Telecommunications", "Transportation and Logistics", 
    "Manufacturing", "Biotechnology", "Consumer Goods"
]

class RandomDataGenerator:
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
      self.df.loc[i, [f'Preference {j+1}' for j in range(self.num_preferences)]] = 0
      specific_industries = random.sample(industries, random.randint(1,5))
      self.df.loc[i, 'Industry'] = ";".join(specific_industries)
      self.df.loc[i, [f'Rank {j+1}' for j in range(self.num_questions)]] = random.sample(range(1, 11), self.num_questions)
    
    for i in range(0, self.num_people * 2):
      same_industry = []
      diff_industry = []
      curr_industry = set(self.df.loc[i, 'Industry'].split(';'))

      start = 0
      stop = 0

      if i < 200:
        start = self.num_people
        stop = self.num_people * 2
      else:
        stop = self.num_people

      for j in range(start, stop):
        temp_industry = set(self.df.loc[j, 'Industry'].split(';'))
        if len(temp_industry.intersection(curr_industry)) > 0:
          same_industry.append(j % self.num_people)
        else:
          diff_industry.append(j % self.num_people)
      
      if len(same_industry) < self.num_preferences:
        same_industry.extend(diff_industry[0:(self.num_preferences-len(same_industry))])

      self.df.loc[i, [f'Preference {j+1}' for j in range(self.num_preferences)]] = random.sample(same_industry, self.num_preferences)

    for i in range(self.num_preferences):
      self.df[f'Preference {i+1}'] = self.df[f'Preference {i+1}'].astype(int)
    
    for i in range(self.num_questions):
      self.df[f'Rank {i+1}'] = self.df[f'Rank {i+1}'].astype(int)
  
  def export(self):
    self.df.to_csv('input_data.csv', index=False)

rg = RandomDataGenerator(200,15,7)
rg.create()
rg.export()