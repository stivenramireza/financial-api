from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.user_schema import User, UserCreate
from src.repositories import user_repository
from src.services import contact_service
from src.middlewares import password_middleware


def get_user_by_id(db: Session, user_id: str) -> User:
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    contact = contact_service.get_contact_by_id(db, user.contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found'
        )

    return contact


def get_user_by_contact_id(db: Session, contact_id: str) -> User:
    return user_repository.get_user_by_contact_id(db, contact_id)


def create_user(db: Session, user: UserCreate) -> User:
    created_contact = contact_service.create_contact(db, user)
    if not created_contact:
        raise HTTPException(
            status_code=409, detail='Contact could not be registered'
        )

    hashed_password = password_middleware.get_password_hash(user.password)
    return user_repository.create_user(
        db, user.username, hashed_password, created_contact.id
    )
