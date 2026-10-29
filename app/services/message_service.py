from app.db.db_entities import Message, User
from app.models.models import MessageDto, MessageModel


def create_message(db, dto: MessageModel, author_id: int) -> MessageDto:
    message = Message(
        conversation_id=dto.conversation_id,
        author_id=author_id,
        content=dto.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return MessageDto.model_validate(message)


def get_message(db, message_id: int) -> MessageDto | None:
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None:
        return None
    return MessageDto.model_validate(message)


def list_messages(db, conversation_id: int, limit: int = 50):
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return [MessageDto.model_validate(m) for m in messages]


def user_exists(db, user_id: int) -> bool:
    return db.query(User).filter(User.id == user_id).first() is not None
