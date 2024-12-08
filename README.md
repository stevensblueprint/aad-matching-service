# Introduction
This is an MVP for the AAD Kin Mentorship Matching Algorithm

# Resources
* [Shared Google Drive](https://drive.google.com/drive/folders/107hANTj3ZX6qOycbk2PjJY76QEWB_CDV)

# Setup

This setup guide requires you to have the following installed on your machine:
 - Python (version 3.10.12)

1. Create a virtual environment to manage packages/libraries:
```
python3 -m venv venv
```

2. Activate the virtual environment:
```
source venv/bin/activate # Linux/Ubuntu
```

3. Install dependencies (packages/libraries)
```
pip install -r "requirements.txt"
```

# Directory Structure
* `data/` - This directory will hold the data for the matching algorithm.
* `processing/` - This directory will hold the code for processing the data.
* `matching_script/` - This directory will hold the code for the matching algorithm.

# TODOS/Notes
* In the output of the matching algorithm script (pairs.csv), 'Mentor Preference Number' and 'Mentee Preference Number' have N/A values for anytime a preference is not in the top 15. Is there a way we can fix this so that AAD can get a better measure of how successful the algorithm was for each person?
* It was noted earlier that less industries yielded higher accuracy (which makes sense). On the Microsoft form we can constrain the number of industries each person is allowed to select. This will 'artificially' increase the accuracy of the algorithm, but I think that it would be beneficial since it elminates outliers who might select a large number of industries
* What else can be added to the pairs.csv output to give a measure of the algorithms success? How can we make that table look more presentable for AAD?