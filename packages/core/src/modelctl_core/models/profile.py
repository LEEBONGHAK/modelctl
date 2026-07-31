from datetime import UTC, datetime
from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(unique=True, index=True)

    description: str | None = None

    provider: str = "openrouter"

    default_model: str | None = None

    launcher: str = "claude"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
