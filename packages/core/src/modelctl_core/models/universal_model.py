from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class UniversalModel(SQLModel, table=True):
    __tablename__ = "models"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    provider: str = Field(index=True)

    model_id: str = Field(
        unique=True,
        index=True,
    )

    name: str

    context_length: int = 0

    prompt_price: float = 0

    completion_price: float = 0

    supports_vision: bool = False

    supports_tools: bool = False

    supports_reasoning: bool = False

    favorite: bool = False

    last_used_at: datetime | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
