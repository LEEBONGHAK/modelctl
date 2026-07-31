from __future__ import annotations

from sqlmodel import Field
from sqlmodel import SQLModel


class UniversalModel(SQLModel, table=True):
    __tablename__ = "models"

    id: int | None = Field(default=None, primary_key=True)

    provider: str = Field(index=True)

    model_id: str = Field(index=True, unique=True)

    display_name: str

    organization: str | None = None

    family: str | None = None

    context_length: int = 0

    prompt_price: float | None = None

    completion_price: float | None = None

    supports_vision: bool = False

    supports_tools: bool = False

    supports_reasoning: bool = False

    metadata: str = "{}"
