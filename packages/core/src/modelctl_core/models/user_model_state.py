from datetime import UTC, datetime
from sqlmodel import Field, SQLModel


class UserModelState(SQLModel, table=True):
    __tablename__ = "user_model_state"

    profile_name: str = Field(
        foreign_key="profiles.name",
        primary_key=True,
    )

    model_id: str = Field(
        foreign_key="models.model_id",
        primary_key=True,
    )

    favorite: bool = False

    pinned: bool = False

    alias: str | None = None

    usage_count: int = 0

    last_used_at: datetime | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
