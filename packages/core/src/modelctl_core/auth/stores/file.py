import json
from pathlib import Path

from platformdirs import user_config_dir

from modelctl_core.auth.base import CredentialStore


class FileStore(CredentialStore):
    def __init__(self, path: Path | None = None):
        self.path = path or Path(user_config_dir("modelctl")) / "credentials.json"

    def _read(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, service: str, key: str, secret: str) -> None:
        data = self._read()
        data.setdefault(service, {})[key] = secret
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, service: str, key: str) -> str | None:
        return self._read().get(service, {}).get(key)

    def delete(self, service: str, key: str) -> None:
        data = self._read()
        service_data = data.get(service, {})
        service_data.pop(key, None)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
