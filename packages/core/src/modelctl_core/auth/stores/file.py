import json
from pathlib import Path

from platformdirs import user_config_dir

from modelctl_core.auth.base import CredentialStore
from modelctl_core.security.private_files import (
    atomic_write_private_text,
    read_private_text,
)


class FileStore(CredentialStore):
    def __init__(self, path: Path | None = None):
        self.path = path or Path(user_config_dir("modelctl")) / "credentials.json"

    def _read(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}

        raw = json.loads(read_private_text(self.path))
        if not isinstance(raw, dict):
            raise ValueError(f"Invalid credential file format: {self.path}")

        data: dict[str, dict[str, str]] = {}
        for service, values in raw.items():
            if not isinstance(service, str) or not isinstance(values, dict):
                raise ValueError(f"Invalid credential file format: {self.path}")
            if not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in values.items()
            ):
                raise ValueError(f"Invalid credential file format: {self.path}")
            data[service] = values
        return data

    def _write(self, data: dict[str, dict[str, str]]) -> None:
        atomic_write_private_text(
            self.path,
            json.dumps(data, indent=2) + "\n",
        )

    def save(self, service: str, key: str, secret: str) -> None:
        data = self._read()
        data.setdefault(service, {})[key] = secret
        self._write(data)

    def load(self, service: str, key: str) -> str | None:
        return self._read().get(service, {}).get(key)

    def delete(self, service: str, key: str) -> None:
        data = self._read()
        service_data = data.get(service)
        if service_data is None:
            return

        service_data.pop(key, None)
        if not service_data:
            data.pop(service, None)
        self._write(data)
