import numpy as np
import pandas as pd
import time

class MatchingAlgorithm:
  def __init__(self, df, num_preferences, num_questions, mentor_weight, mentee_weight):
    self.mentor_df = df[df.iloc[:, 1] == 'Mentor']
    self.mentee_df = df[df.iloc[:, 1] == 'Mentee']
    self.num_preferences = num_preferences
    self.num_questions = num_questions
    self.size = self.mentor_df.shape[0]
    self.mentor_scores = np.zeros((self.size, self.size)) 
    self.mentee_scores = np.zeros((self.size, self.size)) 
    self.mentor_weight = mentor_weight / mentee_weight
    self.mentor_df = self.mentor_df.sort_values(by=self.mentor_df.columns[0])
    self.mentee_df = self.mentee_df.sort_values(by=self.mentee_df.columns[0])
    self.mentor_top_pref = self.mentor_df.iloc[:,2:2+self.num_preferences]
    self.mentee_top_pref = self.mentee_df.iloc[:,2:2+self.num_preferences]

  def create_pairs(self):
    start = time.time()
    self.concat_industry()
    self.calculate_scores()
    self.match_pairs()
    stop = time.time()
    print(f'Created pairs in {round(stop-start,2)} seconds')
    return self.pairs

  def concat_industry(self):
    self.mentor_df.iloc[:,2+self.num_preferences] = self.mentor_df.iloc[:,2+self.num_preferences].apply(lambda x: set(x.split(';')))
    self.mentee_df.iloc[:,2+self.num_preferences] = self.mentee_df.iloc[:,2+self.num_preferences].apply(lambda x: set(x.split(';')))

  def calculate_scores(self):
    # First add to the score based on mentor/mentee preferences
    for i in range(self.size):
      preferences = self.mentor_df.iloc[i, 2:self.num_preferences+2]
      for j, preference in enumerate(preferences):
        self.mentor_scores[i][preference] += self.num_preferences * 100 - 100 * j

    for i in range(self.size):
      preferences = self.mentee_df.iloc[i, 2:self.num_preferences+2]
      for j, preference in enumerate(preferences):
        self.mentee_scores[i][preference] += self.num_preferences * 100 - 100 * j

    # Then see if any industries overlap and calculate residuals of quantitative questions
    temp_mentor_scores = np.zeros((self.size, self.size))
    temp_mentee_scores = np.zeros((self.size, self.size))

    for i in range(self.mentor_df.shape[0]):
      for j in range(self.mentee_df.shape[0]):
        mentor_industries = self.mentor_df.iloc[i, 2 + self.num_preferences]
        mentee_industries = self.mentee_df.iloc[j, 2 + self.num_preferences]
        industries = mentor_industries.intersection(mentee_industries)
        if len(industries) > 0:
          temp_mentor_scores[i][j] = 10 * self.num_questions + 10 * np.sqrt(len(industries))
          temp_mentee_scores[j][i] = 10 * self.num_questions + 10 * np.sqrt(len(industries))

    for i in range(self.mentor_df.shape[0]):
      for j in range(self.mentee_df.shape[0]):
        residual_sum = (10 - (self.mentor_df.iloc[i,3+self.num_preferences:] - self.mentee_df.iloc[j,3+self.num_preferences:]).abs()).sum()
        temp_mentor_scores[i][j] += residual_sum
        temp_mentee_scores[j][i] += residual_sum

    # Normalize the data to range from 0 to self.base - 1 and add to scores
    temp_mentor_scores = (temp_mentor_scores - temp_mentor_scores.min()) * 99 / (temp_mentor_scores.max() - temp_mentor_scores.min())    
    self.mentor_scores += temp_mentor_scores
    temp_mentee_scores = (temp_mentee_scores - temp_mentee_scores.min()) * 99 / (temp_mentee_scores.max() - temp_mentee_scores.min())    
    self.mentee_scores += temp_mentee_scores

    # Create array of mentor and mentee preferences based on the highest score
    self.mentor_preferences = np.zeros((self.size, self.size), dtype = int)
    self.mentee_preferences = np.zeros((self.size, self.size), dtype = int)

    for i in range(self.size):
      self.mentor_preferences[i] = self.mentor_scores[i].argsort()[::-1]
      self.mentee_preferences[i] = self.mentee_scores[i].argsort()[::-1]

  def match_pairs(self):
    self.mentor_preferences = self.mentor_preferences.tolist()
    self.mentee_preferences = self.mentee_preferences.tolist()

    free_mentors = list(range(self.size))
    pairs = {}
    mentor_proposals = dict.fromkeys(free_mentors, [])

    while free_mentors:
      mentor = free_mentors[0]
      mentor_pref = self.mentor_preferences[mentor]

      for mentee in mentor_pref:
        if mentee not in mentor_proposals[mentor]:
          mentor_proposals[mentor].append(mentee)

          if mentee not in pairs.values():
            pairs[mentor] = mentee
            free_mentors.remove(mentor)
            break

          else:
            current_mentor = next(m for m, v in pairs.items() if v == mentee)
            mentee_pref = self.mentee_preferences[mentee]

            if mentee_pref.index(mentor) < mentee_pref.index(current_mentor):
              pairs[mentor] = mentee
              free_mentors.remove(mentor)
              free_mentors.append(current_mentor)
              del pairs[current_mentor]
              break

    self.pairs = pairs

  # Calculate the number of top 10 choice matches
  def output_accuracy(self):
    mentor_matches = 0
    mentee_matches = 0
    for mentor, mentee in self.pairs.items():
      mentor_pref = self.mentor_top_pref.iloc[mentor,:].values.tolist()
      mentee_pref = self.mentee_top_pref.iloc[mentee,:].values.tolist()
      if mentee in mentor_pref:
        mentor_matches += 1
      if mentor in mentee_pref:
        mentee_matches += 1

    print("Mentor accuracy: ", mentor_matches / self.size)
    print("Mentee accuracy: ", mentee_matches / self.size)

df = pd.read_csv('input_data.csv')
matcher = MatchingAlgorithm(df,15,7,15,10)
matcher.create_pairs()
matcher.output_accuracy()