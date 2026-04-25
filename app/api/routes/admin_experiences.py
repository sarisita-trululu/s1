from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.database.session import get_db
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceRead, ExperienceUpdate
from app.services.slug import generate_unique_slug


router = APIRouter(prefix="/api/admin/experiences", tags=["Admin Experiences"])


def get_experience_or_404(experience_id: int, db: Session) -> Experience:
    experience = db.get(Experience, experience_id)
    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia no encontrada.")
    return experience


def validate_spots(capacity: int, available_spots: int) -> None:
    if available_spots > capacity:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Los cupos disponibles no pueden superar la capacidad.",
        )


@router.get("", response_model=list[ExperienceRead], dependencies=[Depends(get_current_admin)])
def list_admin_experiences(db: Annotated[Session, Depends(get_db)]) -> list[Experience]:
    return list(db.scalars(select(Experience).order_by(desc(Experience.date), Experience.id.desc())).all())


@router.post("", response_model=ExperienceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_experience(payload: ExperienceCreate, db: Annotated[Session, Depends(get_db)]) -> Experience:
    available_spots = payload.available_spots if payload.available_spots is not None else payload.capacity
    validate_spots(payload.capacity, available_spots)

    experience = Experience(
        **payload.model_dump(exclude={"slug", "available_spots"}),
        slug=generate_unique_slug(db, Experience, payload.title, payload.slug),
        available_spots=available_spots,
    )
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return experience


@router.get("/{experience_id}", response_model=ExperienceRead, dependencies=[Depends(get_current_admin)])
def get_experience(experience_id: int, db: Annotated[Session, Depends(get_db)]) -> Experience:
    return get_experience_or_404(experience_id, db)


@router.put("/{experience_id}", response_model=ExperienceRead, dependencies=[Depends(get_current_admin)])
def update_experience(
    experience_id: int,
    payload: ExperienceUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Experience:
    experience = get_experience_or_404(experience_id, db)
    updates = payload.model_dump(exclude_unset=True)

    if "title" in updates or "slug" in updates:
        experience.slug = generate_unique_slug(
            db,
            Experience,
            updates.get("title", experience.title),
            updates.get("slug", experience.slug),
            instance_id=experience.id,
        )

    capacity = updates.get("capacity", experience.capacity)
    available_spots = updates.get("available_spots", experience.available_spots)
    validate_spots(capacity, available_spots)

    for field, value in updates.items():
        if field in {"title", "slug"}:
            continue
        setattr(experience, field, value)

    experience.title = updates.get("title", experience.title)
    experience.capacity = capacity
    experience.available_spots = available_spots

    db.commit()
    db.refresh(experience)
    return experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_experience(experience_id: int, db: Annotated[Session, Depends(get_db)]) -> Response:
    experience = get_experience_or_404(experience_id, db)
    db.delete(experience)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
