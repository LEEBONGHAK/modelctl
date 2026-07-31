from pydantic import BaseModel


class Pricing(BaseModel):
    prompt: str

    completion: str


class OpenRouterModel(BaseModel):
    id: str

    name: str

    context_length: int

    pricing: Pricing
