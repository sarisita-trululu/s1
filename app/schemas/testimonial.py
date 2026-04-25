from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TestimonialBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    text: str = Field(min_length=10)
    service_type: str = Field(min_length=2, max_length=120)
    is_visible: bool = True


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    text: str | None = Field(default=None, min_length=10)
    service_type: str | None = Field(default=None, min_length=2, max_length=120)
    is_visible: bool | None = None


class TestimonialRead(TestimonialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
