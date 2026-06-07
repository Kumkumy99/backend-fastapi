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
def get_notes_by_id(id):
    notes=read_notes()
    for note in notes:
        if note["id"]==id:
            return note
    return {"error":"not found"}
def delete_note_by_id(note_id: str):
    notes = read_notes()
    updated_notes = [
        note for note in notes
        if note["id"] != note_id
    ]
    if len(updated_notes) == len(notes):
        return {"error": "Note not found"}
    write_notes(updated_notes)
    return {"message": "Note deleted"}
def update_note(note_id: str, updated_note: Note):
    notes = read_notes()

    for i, note in enumerate(notes):
        if note["id"] == note_id:

            updated_data = updated_note.model_dump()
            updated_data["id"] = note_id

            notes[i] = updated_data

            write_notes(notes)

            return updated_data

    return {"error": "Note not found"}


