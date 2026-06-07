from fastapi import APIRouter
from schema.note import Note

from services.notes_services import (
    create_note,
    get_notes,
    get_notes_by_id,
    delete_note_by_id,
    update_note
)

router = APIRouter()

@router.post("/notes")
def add_notes(note: Note):
    return create_note(note)

@router.get("/notes")
def fetch_notes():
    return get_notes()

@router.get("/notes/{id}")
def get_note_by_id(id: str):
    return get_notes_by_id(id)

@router.delete("/notes/{note_id}")
def delete_note(note_id: str):
    return delete_note_by_id(note_id)

@router.put("/notes/{note_id}")
def edit_note(note_id: str, note: Note):
    return update_note(note_id, note)