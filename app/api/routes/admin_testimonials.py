from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.database.session import get_db
from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialRead, TestimonialUpdate


router = APIRouter(prefix="/api/admin/testimonials", tags=["Admin Testimonials"])


def get_testimonial_or_404(testimonial_id: int, db: Session) -> Testimonial:
    testimonial = db.get(Testimonial, testimonial_id)
    if testimonial is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonio no encontrado.")
    return testimonial


@router.get("", response_model=list[TestimonialRead], dependencies=[Depends(get_current_admin)])
def list_admin_testimonials(db: Annotated[Session, Depends(get_db)]) -> list[Testimonial]:
    return list(db.scalars(select(Testimonial).order_by(desc(Testimonial.created_at), Testimonial.id.desc())).all())


@router.post("", response_model=TestimonialRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_testimonial(payload: TestimonialCreate, db: Annotated[Session, Depends(get_db)]) -> Testimonial:
    testimonial = Testimonial(**payload.model_dump())
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.get("/{testimonial_id}", response_model=TestimonialRead, dependencies=[Depends(get_current_admin)])
def get_testimonial(testimonial_id: int, db: Annotated[Session, Depends(get_db)]) -> Testimonial:
    return get_testimonial_or_404(testimonial_id, db)


@router.put("/{testimonial_id}", response_model=TestimonialRead, dependencies=[Depends(get_current_admin)])
def update_testimonial(
    testimonial_id: int,
    payload: TestimonialUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Testimonial:
    testimonial = get_testimonial_or_404(testimonial_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(testimonial, field, value)

    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_testimonial(testimonial_id: int, db: Annotated[Session, Depends(get_db)]) -> Response:
    testimonial = get_testimonial_or_404(testimonial_id, db)
    db.delete(testimonial)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
