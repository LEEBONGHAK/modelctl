from __future__ import annotations

import re

from modelctl_core.auth.stores.env import EnvironmentStore
from modelctl_core.auth.stores.file import FileStore
from modelctl_core.auth.stores.keyring import KeyringStore

_PROVIDER_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


class CredentialStorageError(RuntimeError):
    """Raised when a credential cannot be stored securely."""


class CredentialService:
    def __init__(
        self,
        environment: EnvironmentStore | None = None,
        keyring_store: KeyringStore | None = None,
        file_store: FileStore | None = None,
    ) -> None:
        self.environment = environment or EnvironmentStore()
        self.keyring = keyring_store or KeyringStore()
        self.file = file_store or FileStore()

    @staticmethod
    def validate_provider(provider: str) -> str:
        if _PROVIDER_ID_PATTERN.fullmatch(provider) is None:
            raise ValueError(
                "Provider ID must contain only lowercase letters, digits, '.', '_', or '-'."
            )
        return provider

    def load(self, provider: str) -> str | None:
        provider = self.validate_provider(provider)

        token = self.environment.load("modelctl", provider)
        if token:
            return token

        try:
            token = self.keyring.load("modelctl", provider)
        except Exception:
            token = None
        if token:
            return token

        return self.file.load("modelctl", provider)

    def save(
        self,
        provider: str,
        token: str,
        *,
        allow_plaintext_file: bool = False,
    ) -> str:
        provider = self.validate_provider(provider)
        token = token.strip()
        if not token:
            raise ValueError("Credential must not be empty.")

        try:
            self.keyring.save("modelctl", provider, token)
            return "keyring"
        except Exception as error:
            if not allow_plaintext_file:
                raise CredentialStorageError(
                    "The operating-system keyring is unavailable. "
                    "Retry with --allow-plaintext-fallback only when you accept "
                    "storing the token in a user-private local file."
                ) from error

        self.file.save("modelctl", provider, token)
        return "file"

    def delete(self, provider: str) -> None:
        provider = self.validate_provider(provider)
        try:
            self.keyring.delete("modelctl", provider)
        except Exception:
            pass
        self.file.delete("modelctl", provider)
