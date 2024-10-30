import csv
import os
import random
from faker import Faker
#pip install Faker
#install any other required libraries


if os.path.exists("dummy_data.csv"):
    os.remove("dummy_data.csv")

fake = Faker() #random name gen library in python

industries = [
    "Mining", "Construction", "Information Technology", "Pharmaceuticals", "Real Estate", "Hospitality", 
    "Energy", "Automotive", "Agriculture", "Telecommunications", "Transportation and Logistics", 
    "Manufacturing", "Biotechnology", "Consumer Goods"
]

#cols
data = [
    ["ID", "Mentor or Mentee?", "Preference 1", "Preference 2", "Preference 3", "Preference 4", 
     "Preference 5", "Preference 6", "Preference 7", "Preference 8", "Preference 9", "Preference 10", 
     "Industry", "Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5", "Rank 6", "Rank 7"]
]

# Generate 200 mentors and 200 mentees with random preferences and rankings
for i in range(400):
    role = "Mentor"
    if(i>=200):
        role = "Mentee"
    
    preferences = random.sample(range(1, 200), 10)
    industry = random.choice(industries)
    ranks = [random.randint(1, 10) for j in range(7)]

    data.append([i, role] + preferences + [industry] + ranks)

#put data in file
file_path = os.path.join("./", "dummy_data.csv")
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Done!")