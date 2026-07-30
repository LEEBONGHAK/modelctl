from datetime import datetime

from sqlmodel import SQLModel, Field


class Model(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )


    provider: str


    model_id: str


    name: str | None = None


    context_length: int | None = None


    input_price: float | None = None


    output_price: float | None = None


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
