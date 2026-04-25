from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    items: list[str] = Field(default_factory=list)
    icon: str | None = Field(default=None, max_length=120)
    order: int = Field(default=0, ge=0)
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, min_length=10)
    items: list[str] | None = None
    icon: str | None = Field(default=None, max_length=120)
    order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ServiceRead(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
