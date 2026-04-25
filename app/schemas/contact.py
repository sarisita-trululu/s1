from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactMessageBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=140)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=60)
    reason: str = Field(min_length=2, max_length=140)
    message: str = Field(min_length=10)


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessageAdminCreate(ContactMessageBase):
    is_read: bool = False


class ContactMessageUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=140)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=60)
    reason: str | None = Field(default=None, min_length=2, max_length=140)
    message: str | None = Field(default=None, min_length=10)
    is_read: bool | None = None


class ContactMessageRead(ContactMessageBase):
    id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactSubmitResponse(BaseModel):
    message: str
