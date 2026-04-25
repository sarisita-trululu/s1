from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BlogPostBase(BaseModel):
    title: str = Field(min_length=3, max_length=220)
    slug: str | None = Field(default=None, min_length=3, max_length=240)
    excerpt: str = Field(min_length=10)
    content: str = Field(min_length=30)
    category: str = Field(min_length=2, max_length=120)
    cover_image: str | None = Field(default=None, max_length=500)
    is_published: bool = False
    published_at: datetime | None = None


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=220)
    slug: str | None = Field(default=None, min_length=3, max_length=240)
    excerpt: str | None = Field(default=None, min_length=10)
    content: str | None = Field(default=None, min_length=30)
    category: str | None = Field(default=None, min_length=2, max_length=120)
    cover_image: str | None = Field(default=None, max_length=500)
    is_published: bool | None = None
    published_at: datetime | None = None


class BlogPostRead(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
