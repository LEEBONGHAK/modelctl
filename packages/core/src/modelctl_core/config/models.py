from pathlib import Path

from pydantic import BaseModel


class AppConfig(BaseModel):
    default_provider: str | None = None

    default_launcher: str | None = None

    default_model: str | None = None

    database_path: Path

    cache_dir: Path
