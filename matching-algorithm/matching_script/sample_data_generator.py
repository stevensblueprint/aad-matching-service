import numpy as np
import pandas as pd
import random

industries = [
    "Mining", "Construction", "Information Technology", "Pharmaceuticals", "Real Estate", "Hospitality", 
    "Energy", "Automotive", "Agriculture", "Telecommunications", "Transportation and Logistics", 
    "Manufacturing", "Biotechnology", "Consumer Goods"
]

genders = [
  "Male", "Female", "Non-binary"
]

gender_weighting = [
  0.49, 0.49, 0.02
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

    for i in range(0, self.num_people * 2):
      self.df.loc[i, [f'Preference {j+1}' for j in range(self.num_preferences)]] = 0
      specific_industries = random.sample(industries, random.randint(1,3))
      self.df.loc[i, 'Industry'] = ";".join(specific_industries)
      self.df.loc[i, [f'Rank {j+1}' for j in range(self.num_questions)]] = random.sample(range(1, 11), self.num_questions)
      self.df.loc[i, 'Gender'] = random.choices(genders, weights = gender_weighting, k = 1)[0]
      gender_preferences = [
        self.df.loc[i, 'Gender'], "No Preference"
      ]
      self.df.loc[i, 'Gender Preference'] = random.choices(gender_preferences, weights = [0.2,0.8], k = 1)[0]

    for i in range(0, self.num_people * 2):
      same_industry_gender = []
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
        if self.df.loc[i, 'Gender Preference'] != "No Preference":
          if len(temp_industry.intersection(curr_industry)) > 0 and self.df.loc[i, 'Gender Preference'] == self.df.loc[j, 'Gender']:
            same_industry_gender.append(j % self.num_people)
          elif len(temp_industry.intersection(curr_industry)) > 0:
            same_industry.append(j % self.num_people)
          else:
            diff_industry.append(j % self.num_people)
        else:
          if len(temp_industry.intersection(curr_industry)) > 0:
            same_industry_gender.append(j % self.num_people)
          else:
            same_industry.append(j % self.num_people)
      
      if len(same_industry_gender) < self.num_preferences:
        same_industry_gender.extend(same_industry[0:(self.num_preferences-len(same_industry_gender))])

      if len(same_industry_gender) < self.num_preferences:
        same_industry_gender.extend(diff_industry[0:(self.num_preferences-len(same_industry_gender))])

      self.df.loc[i, [f'Preference {j+1}' for j in range(self.num_preferences)]] = random.sample(same_industry_gender, self.num_preferences)

    for i in range(self.num_preferences):
      self.df[f'Preference {i+1}'] = self.df[f'Preference {i+1}'].astype(int)
    
    for i in range(self.num_questions):
      self.df[f'Rank {i+1}'] = self.df[f'Rank {i+1}'].astype(int)
  
  def export(self):
    mentor_df = self.df.iloc[:200,:]
    mentee_df = self.df.iloc[200:,:]
    mentor_df.to_csv('mentor_input_data.csv', index=False)
    mentee_df.to_csv('mentee_input_data.csv', index=False)

rg = RandomDataGenerator(200,15,7)
rg.create()
rg.export()