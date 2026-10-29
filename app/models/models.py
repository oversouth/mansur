# DTOs for the external API (Pydantic models)
# Internal SQLAlchemy models live in app/db/db_entities.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateUserDto(BaseModel):
    username: str
    password: str


class UserDto(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateConversationDto(BaseModel):
    name: Optional[str] = None
    participant_ids: list[int] = []


class ConversationDto(BaseModel):
    id: int
    name: Optional[str] = None
    created_at: datetime
    participant_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)


class MessageModel(BaseModel):
    conversation_id: int
    content: str


class MessageDto(BaseModel):
    id: int
    conversation_id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
