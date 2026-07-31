from dataclasses import dataclass


@dataclass(slots=True)
class ModelView:
    provider: str

    model_id: str

    display_name: str

    family: str | None

    context_length: int

    prompt_price: float

    completion_price: float

    supports_vision: bool

    supports_reasoning: bool

    supports_tools: bool

    favorite: bool

    pinned: bool

    usage_count: int
