from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.database.session import get_db
from app.models.contact import ContactMessage
from app.schemas.contact import (
    ContactMessageAdminCreate,
    ContactMessageRead,
    ContactMessageUpdate,
)


router = APIRouter(prefix="/api/admin/contact-messages", tags=["Admin Contact Messages"])


def get_contact_message_or_404(message_id: int, db: Session) -> ContactMessage:
    message = db.get(ContactMessage, message_id)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado.")
    return message


@router.get("", response_model=list[ContactMessageRead], dependencies=[Depends(get_current_admin)])
def list_contact_messages(db: Annotated[Session, Depends(get_db)]) -> list[ContactMessage]:
    return list(
        db.scalars(
            select(ContactMessage)
            .order_by(asc(ContactMessage.is_read), desc(ContactMessage.created_at), ContactMessage.id.desc())
        ).all()
    )


@router.post("", response_model=ContactMessageRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_contact_message_admin(
    payload: ContactMessageAdminCreate,
    db: Annotated[Session, Depends(get_db)],
) -> ContactMessage:
    message = ContactMessage(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/{message_id}", response_model=ContactMessageRead, dependencies=[Depends(get_current_admin)])
def get_contact_message(message_id: int, db: Annotated[Session, Depends(get_db)]) -> ContactMessage:
    return get_contact_message_or_404(message_id, db)


@router.put("/{message_id}", response_model=ContactMessageRead, dependencies=[Depends(get_current_admin)])
def update_contact_message(
    message_id: int,
    payload: ContactMessageUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> ContactMessage:
    message = get_contact_message_or_404(message_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(message, field, value)

    db.commit()
    db.refresh(message)
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_contact_message(message_id: int, db: Annotated[Session, Depends(get_db)]) -> Response:
    message = get_contact_message_or_404(message_id, db)
    db.delete(message)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
