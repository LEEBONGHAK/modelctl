from pydantic import BaseModel


class ModelctlConfig(BaseModel):
    provider: str | None = None

    default_model: str | None = None

    launcher: str = "claude"

    database_path: str
