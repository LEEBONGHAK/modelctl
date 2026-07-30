from pathlib import Path

import tomllib
import tomli_w
from platformdirs import user_config_dir, user_cache_dir

from .models import AppConfig


class ConfigManager:
    def __init__(self):

        self.config_dir = Path(user_config_dir("modelctl"))

        self.config_file = self.config_dir / "config.toml"

    def load(self):

        if not self.config_file.exists():
            return self.create_default()

        with open(
            self.config_file,
            "rb",
        ) as f:
            data = tomllib.load(f)

        return AppConfig.model_validate(data)

    def save(
        self,
        config: AppConfig,
    ):

        self.config_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.config_file,
            "wb",
        ) as f:
            tomli_w.dump(
                config.model_dump(mode="python"),
                f,
            )

    def create_default(self):

        cfg = AppConfig(
            database_path=(self.config_dir / "modelctl.db"),
            cache_dir=Path(user_cache_dir("modelctl")),
        )

        self.save(cfg)

        return cfg
