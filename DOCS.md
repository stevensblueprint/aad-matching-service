# Processing Steps

1. (Optional): For testing purposes you can generate reponses that mimic the structure of the matching form. To do this, run the following command:
```bash
python generate_matching_responses.py
```
*Note: The script above requires you to have a list of mentors and mentees in .csv format. You can reference mentee_directory_200.csv for reference*

2. Run the following command to process the data:
```bash
python preprocessing.py
```

This will generate a file called `processed_data.csv` which can be used in the matching algorithm.

# Bugs and Potential Issues:
- What if users list the same preference multiple times?
- What if users input a float?
- How can we handle errors without interupting the entire process? Ideally we automatically process as much as possible and then output/highlight errors at the end
- How do we handle a different number of mentors and mentees