from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteSettingBase(BaseModel):
    key: str = Field(min_length=2, max_length=120)
    value: str = Field(min_length=1)


class SiteSettingCreate(SiteSettingBase):
    pass


class SiteSettingUpdate(BaseModel):
    key: str | None = Field(default=None, min_length=2, max_length=120)
    value: str | None = Field(default=None, min_length=1)


class SiteSettingRead(SiteSettingBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
