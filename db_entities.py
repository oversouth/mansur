from sqlalchemy import(
    BigInteger,DateTime,
    ForeignKey, String,
    Text
)
from sqlalchemy.orm import(
    DeclarativeBase,
    Mapped,
    mapped_column
)
from enum import Enum
class Base(DeclarativeBase):
    pass

class UserStatus(str, Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    BUSY = "Busy"
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        Autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(63),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        BigInteger,
        String(255),
        nullable=False
    )
    avatar_url: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Offline"
    )

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    members: Mapped[list["ConversationParticipant"]] = mapped_column(
        ForeignKey("conversation_participants.id"),
        nullable=False
    )
    ConversationName: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

class Message(Base):
    __tablename__ = "messages"
