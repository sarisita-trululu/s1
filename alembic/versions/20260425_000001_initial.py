"""Initial schema for Nuby Arango Perez backend."""

from alembic import op
import sqlalchemy as sa


revision = "20260425_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="admin"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("items", sa.JSON(), nullable=False),
        sa.Column("icon", sa.String(length=120), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
    )
    op.create_index(op.f("ix_services_id"), "services", ["id"], unique=False)

    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("available_spots", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("proximamente", "cupos_abiertos", "finalizada", name="experience_status"),
            nullable=False,
            server_default="proximamente",
        ),
        sa.Column("cover_image", sa.String(length=500), nullable=True),
        sa.Column("gallery_images", sa.JSON(), nullable=False),
        sa.Column("whatsapp_message", sa.Text(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_experiences")),
        sa.UniqueConstraint("slug", name=op.f("uq_experiences_slug")),
    )
    op.create_index(op.f("ix_experiences_id"), "experiences", ["id"], unique=False)
    op.create_index(op.f("ix_experiences_slug"), "experiences", ["slug"], unique=False)

    op.create_table(
        "blog_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("slug", sa.String(length=240), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("cover_image", sa.String(length=500), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blog_posts")),
        sa.UniqueConstraint("slug", name=op.f("uq_blog_posts_slug")),
    )
    op.create_index(op.f("ix_blog_posts_id"), "blog_posts", ["id"], unique=False)
    op.create_index(op.f("ix_blog_posts_slug"), "blog_posts", ["slug"], unique=False)

    op.create_table(
        "testimonials",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("service_type", sa.String(length=120), nullable=False),
        sa.Column("is_visible", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_testimonials")),
    )
    op.create_index(op.f("ix_testimonials_id"), "testimonials", ["id"], unique=False)

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=140), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=60), nullable=True),
        sa.Column("reason", sa.String(length=140), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contact_messages")),
    )
    op.create_index(op.f("ix_contact_messages_email"), "contact_messages", ["email"], unique=False)
    op.create_index(op.f("ix_contact_messages_id"), "contact_messages", ["id"], unique=False)

    op.create_table(
        "site_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_site_settings")),
        sa.UniqueConstraint("key", name=op.f("uq_site_settings_key")),
    )
    op.create_index(op.f("ix_site_settings_id"), "site_settings", ["id"], unique=False)
    op.create_index(op.f("ix_site_settings_key"), "site_settings", ["key"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_site_settings_key"), table_name="site_settings")
    op.drop_index(op.f("ix_site_settings_id"), table_name="site_settings")
    op.drop_table("site_settings")

    op.drop_index(op.f("ix_contact_messages_id"), table_name="contact_messages")
    op.drop_index(op.f("ix_contact_messages_email"), table_name="contact_messages")
    op.drop_table("contact_messages")

    op.drop_index(op.f("ix_testimonials_id"), table_name="testimonials")
    op.drop_table("testimonials")

    op.drop_index(op.f("ix_blog_posts_slug"), table_name="blog_posts")
    op.drop_index(op.f("ix_blog_posts_id"), table_name="blog_posts")
    op.drop_table("blog_posts")

    op.drop_index(op.f("ix_experiences_slug"), table_name="experiences")
    op.drop_index(op.f("ix_experiences_id"), table_name="experiences")
    op.drop_table("experiences")

    op.drop_index(op.f("ix_services_id"), table_name="services")
    op.drop_table("services")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    sa.Enum(name="experience_status").drop(op.get_bind(), checkfirst=False)
