import numpy as np
import pandas as pd

class MatchingAlgorithm:
  def __init__(self, df, num_preferences, num_questions, base = 100, mentor_weight = 15, mentee_weight = 10):
    self.mentor_df = df[df.iloc[:, 1] == 'Mentor']
    self.mentee_df = df[df.iloc[:, 1] == 'Mentee']
    self.num_preferences = num_preferences
    self.num_questions = num_questions
    self.size = self.mentor_df.shape[0]
    self.scores = np.zeros((self.size, self.size)) # row is mentor, column is mentee
    self.base = base
    self.mentor_weight = mentor_weight # Can change this to increase the weight of mentor preferences
    self.mentee_weight = mentee_weight # Must be at least 10
    self.mentor_df = self.mentor_df.sort_values(by=self.mentor_df.columns[0])
    self.mentee_df = self.mentee_df.sort_values(by=self.mentee_df.columns[0])

  def create_pairs(self):
    self.concat_industry()
    self.calculate_scores()
    self.match_pairs()
    return self.pairs

  def concat_industry(self):
    self.mentor_df.iloc[:,2+self.num_preferences] = self.mentor_df.iloc[:,2+self.num_preferences].apply(lambda x: set(x.split(';')))
    self.mentee_df.iloc[:,2+self.num_preferences] = self.mentee_df.iloc[:,2+self.num_preferences].apply(lambda x: set(x.split(';')))

  def calculate_scores(self):
    # First add to the score based on mentor/mentee preferences
    for i in range(self.size):
      preferences = self.mentor_df.iloc[i, 2:self.num_preferences+2]
      for j, preference in enumerate(preferences):
        self.scores[i][preference] += self.base * self.mentor_weight - self.base * j

    for i in range(self.size):
      preferences = self.mentee_df.iloc[i, 2:self.num_preferences+2]
      for j, preference in enumerate(preferences):
        self.scores[preference][i] += self.base * self.mentee_weight - self.base * j

    # Then see if any industries overlap and calculate residuals of quantitative questions
    temp_scores = np.zeros((self.size, self.size))

    for i in range(self.mentor_df.shape[0]):
      for j in range(self.mentee_df.shape[0]):
        mentor_industries = self.mentor_df.iloc[i, 2 + self.num_preferences]
        mentee_industries = self.mentee_df.iloc[j, 2 + self.num_preferences]
        industries = mentor_industries.intersection(mentee_industries)
        if len(industries) > 0:
          temp_scores[i][j] = 10 * self.num_questions + 10 * np.sqrt(len(industries))

    for i in range(self.mentor_df.shape[0]):
      for j in range(self.mentee_df.shape[0]):
        residual_sum = (10 - (self.mentor_df.iloc[i,3+self.num_preferences:] - self.mentee_df.iloc[j,3+self.num_preferences:]).abs()).sum()
        temp_scores[i][j] += residual_sum

    # Normalize the data to range from 0 to self.base - 1 and add to scores
    temp_scores = (temp_scores - temp_scores.min()) * (self.base - 1) / (temp_scores.max() - temp_scores.min())
    self.scores += temp_scores

    # Create array of mentor and mentee preferences based on the highest score
    self.mentor_preferences = np.zeros((self.size, self.size), dtype = int)
    self.mentee_preferences = np.zeros((self.size, self.size), dtype = int)

    for i in range(self.size):
      self.mentor_preferences[i] = self.scores[i].argsort()[::-1]
      self.mentee_preferences[i] = self.scores[:,i].argsort()[::-1]

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
      mentor_pref = self.mentor_preferences[mentor]
      mentee_pref = self.mentee_preferences[mentee]
      if mentor_pref.index(mentee) < self.num_preferences:
        mentor_matches += 1
      if mentee_pref.index(mentor) < self.num_preferences:
        mentee_matches += 1

    print("Mentor accuracy: ", mentor_matches / self.size)
    print("Mentee accuracy: ", mentee_matches / self.size)

class NameParser:
  def __init__(self, pairs, mentors, mentees):
    self.pairs = pairs
    self.mentors = mentors
    self.mentees = mentees

  def parse(self):
    self.pairs = pd.DataFrame(self.pairs, index=[0]).melt(var_name='Mentor', value_name='Mentee')
    self.pairs = pd.merge(self.pairs, self.mentors, left_on='Mentor', right_on=self.mentors.columns[0])
    self.pairs = pd.merge(self.pairs, self.mentees, left_on='Mentee', right_on=self.mentees.columns[0])
    self.pairs = self.pairs.iloc[:, 2:]
    self.pairs.to_csv('pairs.csv')

df = pd.read_csv('test3.csv')
df2 = pd.read_csv('mentors.csv')
df3 = pd.read_csv('mentees.csv')
# matcher for test.csv
# matcher = MatchingAlgorithm(df,1,3,100,15,10)
# matcher for test2.csv 
# matcher = MatchingAlgorithm(df,5,5,100,15,10)
# matcher for test3.csv
matcher = MatchingAlgorithm(df,10,7,100,15,10)
matcher.create_pairs()
parser = NameParser(matcher.pairs,df2,df3)
parser.parse()