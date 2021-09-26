# Description of the Tense Switcher
Automatically changes the tense of any English text.
Inputs:
- Input: "" <<< text you want to put into another tense.
- Tense: "" <<< either future, past, present
Returns:
- Sentence in target tense.

### Install pip first
    sudo apt-get install python3-pip
### Then install virtualenv using pip3
    sudo pip3 install virtualenv 

# Install all dependencies etc.
    Run 'bash start.sh'
    Test app with 'python3 app.py'
    Test server with 'uvicorn main:app'

# Sample 
    {
        "input": "The sun is shining.",
        "tense": "past",
        "output": "string"
    }
    {
        "output": "The sun was shining."
    }

# Run tests
    python3 -m pytest

# Run once locally
    python3 app.py

# Run as FastAPI server locally
    uvicorn main:app

This server is based on tenseflow by Ben Dichter.