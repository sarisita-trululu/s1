from datetime import date as date_type, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.experience import ExperienceStatus


class ExperienceBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    slug: str | None = Field(default=None, min_length=3, max_length=220)
    description: str = Field(min_length=20)
    date: date_type
    location: str = Field(min_length=3, max_length=255)
    capacity: int = Field(gt=0)
    available_spots: int | None = Field(default=None, ge=0)
    status: ExperienceStatus = ExperienceStatus.proximamente
    cover_image: str | None = Field(default=None, max_length=500)
    gallery_images: list[str] = Field(default_factory=list)
    whatsapp_message: str | None = None
    is_published: bool = False

    @model_validator(mode="after")
    def validate_spots(self):
        if self.available_spots is not None and self.available_spots > self.capacity:
            raise ValueError("Los cupos disponibles no pueden superar la capacidad.")
        return self


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    slug: str | None = Field(default=None, min_length=3, max_length=220)
    description: str | None = Field(default=None, min_length=20)
    date: date_type | None = None
    location: str | None = Field(default=None, min_length=3, max_length=255)
    capacity: int | None = Field(default=None, gt=0)
    available_spots: int | None = Field(default=None, ge=0)
    status: ExperienceStatus | None = None
    cover_image: str | None = Field(default=None, max_length=500)
    gallery_images: list[str] | None = None
    whatsapp_message: str | None = None
    is_published: bool | None = None


class ExperienceRead(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    date: date_type
    location: str
    capacity: int
    available_spots: int
    status: ExperienceStatus
    cover_image: str | None
    gallery_images: list[str]
    whatsapp_message: str | None
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
