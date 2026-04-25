from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Testimonial(Base, TimestampMixin):
    __tablename__ = "testimonials"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    service_type: Mapped[str] = mapped_column(String(120), nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
