from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.models import MessageDto, MessageModel
from app.services import message_service

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageDto, status_code=201)
def create_message(
    dto: MessageModel, author_id: int, db: Session = Depends(get_db)
):
    if not message_service.user_exists(db, author_id):
        raise HTTPException(status_code=404, detail="author not found")
    return message_service.create_message(db, dto, author_id)


@router.get("/{message_id}", response_model=MessageDto)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = message_service.get_message(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="message not found")
    return message


@router.get(
    "/conversations/{conversation_id}",
    response_model=list[MessageDto],
)
def list_messages(
    conversation_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return message_service.list_messages(db, conversation_id, limit)
