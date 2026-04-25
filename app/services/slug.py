import re
import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return slug


def generate_unique_slug(
    db: Session,
    model,
    title: str,
    slug: str | None = None,
    instance_id: int | None = None,
) -> str:
    base_slug = slugify(slug or title) or "item"
    candidate = base_slug
    index = 2

    while True:
        query = select(model.id).where(model.slug == candidate)
        if instance_id is not None:
            query = query.where(model.id != instance_id)

        existing = db.scalar(query)
        if existing is None:
            return candidate

        candidate = f"{base_slug}-{index}"
        index += 1
