# Introduction
This directory will hold the code for the matching algorithm. The matching algorithm will be written in Python. There are 2 tentative approaches we have for connecting
the matching algorithm to the client:

1. Compile the program to WebAssembly and run it in the browser.
2. Run the program on server and have the client send requests to the server.

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

# TODOS:
- [X] Write the matching algorithm.
- [X] Write the processing code.
- [ ] Refactor code with pydantic or another library to connect matching-script and processing
- [ ] Write a function to generate IDs for the Directory
