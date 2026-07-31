from pydantic import BaseModel


class ModelctlConfig(BaseModel):
    provider: str = "openrouter"

    default_model: str | None = None

    theme: str = "auto"

    database_path: str

    plugin_dir: str
