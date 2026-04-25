import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ExperienceStatus(str, enum.Enum):
    proximamente = "proximamente"
    cupos_abiertos = "cupos_abiertos"
    finalizada = "finalizada"


class Experience(Base, TimestampMixin):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    available_spots: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ExperienceStatus] = mapped_column(
        Enum(ExperienceStatus, name="experience_status"),
        default=ExperienceStatus.proximamente,
        nullable=False,
    )
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gallery_images: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    whatsapp_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
