from app.db.db_entities import (
    Conversation,
    ConversationParticipant,
    User,
)
from app.models.models import ConversationDto, CreateConversationDto


def create_conversation(db, dto: CreateConversationDto) -> ConversationDto:
    conversation = Conversation(name=dto.name)
    db.add(conversation)
    db.flush()

    participant_ids = set(dto.participant_ids)
    if participant_ids:
        existing = (
            db.query(User.id)
            .filter(User.id.in_(participant_ids))
            .all()
        )
        existing_ids = {row[0] for row in existing}
        participant_ids &= existing_ids

    for user_id in participant_ids:
        db.add(
            ConversationParticipant(
                conversation_id=conversation.id,
                user_id=user_id,
            )
        )

    db.commit()
    db.refresh(conversation)
    return _to_dto(db, conversation)


def get_conversation(db, conversation_id: int) -> ConversationDto | None:
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if conversation is None:
        return None
    return _to_dto(db, conversation)


def list_conversations(db):
    conversations = db.query(Conversation).all()
    return [_to_dto(db, c) for c in conversations]


def _to_dto(db, conversation: Conversation) -> ConversationDto:
    participant_ids = [
        row[0]
        for row in db.query(ConversationParticipant.user_id)
        .filter(ConversationParticipant.conversation_id == conversation.id)
        .all()
    ]
    return ConversationDto(
        id=conversation.id,
        name=conversation.name,
        created_at=conversation.created_at,
        participant_ids=participant_ids,
    )
