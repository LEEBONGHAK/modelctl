import json
from pathlib import Path


class ConfigManager:
    def __init__(
        self,
        path: Path,
    ):

        self.path = path

    def load(self):

        if not self.path.exists():
            return {}

        return json.loads(self.path.read_text())

    def save(
        self,
        data,
    ):

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
            )
        )

    def update_model(
        self,
        provider,
        model,
    ):

        config = self.load()

        config["provider"] = provider

        config["default_model"] = model

        self.save(config)
