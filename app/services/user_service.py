import hashlib

from app.db.db_entities import User, UserStatus
from app.models.models import CreateUserDto, UserDto


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(db, dto: CreateUserDto) -> UserDto:
    user = User(
        username=dto.username,
        email=f"{dto.username}@mansur.local",
        password_hash=_hash_password(dto.password),
        avatar_url=None,
        status=UserStatus.OFFLINE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserDto.model_validate(user)


def get_user_by_username(db, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db):
    return db.query(User).all()
