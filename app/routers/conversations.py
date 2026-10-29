from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.models import (
    ConversationDto,
    CreateConversationDto,
)
from app.services import conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationDto, status_code=201)
def create_conversation(
    dto: CreateConversationDto, db: Session = Depends(get_db)
):
    return conversation_service.create_conversation(db, dto)


@router.get("/", response_model=list[ConversationDto])
def list_conversations(db: Session = Depends(get_db)):
    return conversation_service.list_conversations(db)


@router.get("/{conversation_id}", response_model=ConversationDto)
def get_conversation(
    conversation_id: int, db: Session = Depends(get_db)
):
    conversation = conversation_service.get_conversation(
        db, conversation_id
    )
    if conversation is None:
        raise HTTPException(
            status_code=404, detail="conversation not found"
        )
    return conversation
