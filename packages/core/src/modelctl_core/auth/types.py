from dataclasses import dataclass


@dataclass(slots=True)
class Credential:
    api_key: str | None = None

    endpoint: str | None = None

    organization: str | None = None
