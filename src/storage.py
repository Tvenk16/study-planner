
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "exams.json"


def load_exams():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE) as file:
            return json.load(file)["exams"]
    
    except (json.JSONDecodeError, KeyError):

        sys.exit(f"Error: {DATA_FILE.name} is damaged. Fix or delete it, then try again.")


def save_exams(exams):
   
    with open(DATA_FILE, "w") as file:
        json.dump({"exams": exams}, file, indent=2)



# """Handles saving and loading all of the exam data for the study planner.

#Every exam I add, along with its date and topics, gets stored in a file called
#exams.json in the main project folder. This file has two jobs: load_exams() reads
#that file and gives the rest of the program a list of exams to work with, and
#save_exams() writes the updated list back after something changes, like adding an
#exam or checking off a topic. Keeping all the file reading and writing in one place
#means the rest of the code never has to worry about how the data is stored. If the
#file doesn't exist yet (like the first time someone runs the program), it just
#starts with an empty list instead of crashing. If the file is broken, it stops and
#tells the user instead of overwriting it, so nobody loses their saved exams.
#"""