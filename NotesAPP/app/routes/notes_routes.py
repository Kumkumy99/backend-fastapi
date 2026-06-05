from fastapi import APIRouter
from schema.note import Note
from services.notes_services import (
    create_note,
    get_notes
)
router=APIRouter()
@router.post("/notes")
def add_notes(note:Note):
    return create_note(note)
@router.get("/notes")
def fetch_notes():
    return get_notes()