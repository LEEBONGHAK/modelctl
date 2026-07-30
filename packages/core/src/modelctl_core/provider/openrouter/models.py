from pydantic import BaseModel


class Pricing(BaseModel):

    prompt: str

    completion: str


class Architecture(BaseModel):

    modality: str | None = None

    tokenizer: str | None = None


class OpenRouterModel(BaseModel):

    id: str

    name: str

    context_length: int

    architecture: Architecture | None = None

    pricing: Pricing