from pathlib import Path

import tomllib
from pydantic import BaseModel

from modelctl.core.paths import config_file


class ModelctlConfig(BaseModel):

    default_launcher: str = "claude-code"

    default_provider: str = "openrouter"

    default_model: str | None = None



def save_config(
    config: ModelctlConfig
):

    path = config_file()

    content = f"""
default_launcher="{config.default_launcher}"
default_provider="{config.default_provider}"
"""

    path.write_text(
        content.strip(),
        encoding="utf-8"
    )



def load_config() -> ModelctlConfig:

    path = config_file()

    if not path.exists():

        return ModelctlConfig()


    with path.open(
        "rb"
    ) as f:

        data = tomllib.load(f)


    return ModelctlConfig(
        **data
    )
