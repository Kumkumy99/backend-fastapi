import json
from schema.note import Note
from typing import List
FILE_PATH="data/data.json"
def read_notes():
    with open(FILE_PATH,"r") as f:
        return json.load(f)
def write_notes(notes:List[dict]):
    with open(FILE_PATH, "w") as f:
        json.dump(notes, f)
def get_notes():
    return read_notes()
def create_note(note: Note):
    notes = read_notes()
    notes.append(note.model_dump())   
    write_notes(notes)
    return note


