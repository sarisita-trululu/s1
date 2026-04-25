from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.database.session import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate


router = APIRouter(prefix="/api/admin/services", tags=["Admin Services"])


def get_service_or_404(service_id: int, db: Session) -> Service:
    service = db.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado.")
    return service


@router.get("", response_model=list[ServiceRead], dependencies=[Depends(get_current_admin)])
def list_admin_services(db: Annotated[Session, Depends(get_db)]) -> list[Service]:
    return list(db.scalars(select(Service).order_by(Service.order.asc(), Service.id.asc())).all())


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_service(payload: ServiceCreate, db: Annotated[Session, Depends(get_db)]) -> Service:
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.get("/{service_id}", response_model=ServiceRead, dependencies=[Depends(get_current_admin)])
def get_service(service_id: int, db: Annotated[Session, Depends(get_db)]) -> Service:
    return get_service_or_404(service_id, db)


@router.put("/{service_id}", response_model=ServiceRead, dependencies=[Depends(get_current_admin)])
def update_service(service_id: int, payload: ServiceUpdate, db: Annotated[Session, Depends(get_db)]) -> Service:
    service = get_service_or_404(service_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_service(service_id: int, db: Annotated[Session, Depends(get_db)]) -> Response:
    service = get_service_or_404(service_id, db)
    db.delete(service)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
