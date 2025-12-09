from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields shared by create and update requests."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the note")
    content: str = Field(..., min_length=1, description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating an existing note (full update)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated title of the note")
    content: Optional[str] = Field(None, min_length=1, description="Updated content/body of the note")


# PUBLIC_INTERFACE
class Note(NoteBase):
    """Full note representation returned by the API."""
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True
