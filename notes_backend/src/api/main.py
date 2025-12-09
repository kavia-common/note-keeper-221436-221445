from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware

from .schemas import Note, NoteCreate, NoteUpdate

# FastAPI app with OpenAPI metadata and tags
app = FastAPI(
    title="Notes API",
    description="A simple Notes REST API providing CRUD operations over an in-memory store.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health and service status"},
        {"name": "notes", "description": "CRUD operations for notes"},
    ],
)

# CORS configuration (allow localhost and common dev hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*",  # keep permissive for preview environments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
NOTES: Dict[int, Note] = {}
NEXT_ID: int = 1


def _now_utc() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Simple health check endpoint to verify service is running."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    tags=["notes"],
    summary="Create a note",
)
def create_note(payload: NoteCreate):
    """Create a new note with auto-incremented ID.

    Parameters:
    - payload: NoteCreate - title and content of the note

    Returns:
    - Note - the created note resource with id and timestamps
    """
    global NEXT_ID
    note_id = NEXT_ID
    NEXT_ID += 1

    now = _now_utc()
    note = Note(id=note_id, title=payload.title, content=payload.content, created_at=now, updated_at=now)
    NOTES[note_id] = note
    return note


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    tags=["notes"],
    summary="List notes",
)
def list_notes():
    """List all notes in insertion order (by id ascending)."""
    return [NOTES[k] for k in sorted(NOTES.keys())]


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Retrieve a note",
)
def get_note(
    note_id: int = Path(..., ge=1, description="The ID of the note to retrieve"),
):
    """Retrieve a single note by ID.

    Returns 404 if the note doesn't exist.
    """
    note = NOTES.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Update a note",
)
def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1, description="The ID of the note to update"),
):
    """Update an existing note by ID.

    Allows updating title and/or content. Returns 404 if the note doesn't exist.
    """
    existing = NOTES.get(note_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updated_title = payload.title if payload.title is not None else existing.title
    updated_content = payload.content if payload.content is not None else existing.content

    updated = Note(
        id=existing.id,
        title=updated_title,
        content=updated_content,
        created_at=existing.created_at,
        updated_at=_now_utc(),
    )
    NOTES[note_id] = updated
    return updated


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["notes"],
    summary="Delete a note",
)
def delete_note(
    note_id: int = Path(..., ge=1, description="The ID of the note to delete"),
):
    """Delete a note by ID.

    Returns 204 on success or 404 if the note is missing.
    """
    if note_id not in NOTES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    del NOTES[note_id]
    # Returning None results in a 204 No Content as configured
    return None
