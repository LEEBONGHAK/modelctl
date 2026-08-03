import pytest

from modelctl_core.auth.service import CredentialService, CredentialStorageError
from modelctl_core.auth.stores.file import FileStore


class EmptyEnvironment:
    def load(self, service, key):
        return None


class FailingKeyring:
    def save(self, service, key, secret):
        raise RuntimeError("keyring unavailable")

    def load(self, service, key):
        raise RuntimeError("keyring unavailable")

    def delete(self, service, key):
        raise RuntimeError("keyring unavailable")


class WorkingKeyring:
    def __init__(self):
        self.value = None

    def save(self, service, key, secret):
        self.value = secret

    def load(self, service, key):
        return self.value

    def delete(self, service, key):
        self.value = None


def test_keyring_failure_does_not_silently_write_plaintext(tmp_path):
    file_store = FileStore(tmp_path / "credentials.json")
    service = CredentialService(EmptyEnvironment(), FailingKeyring(), file_store)

    with pytest.raises(CredentialStorageError, match="keyring is unavailable"):
        service.save("openrouter", "secret-token")

    assert not file_store.path.exists()


def test_plaintext_fallback_requires_explicit_opt_in(tmp_path):
    file_store = FileStore(tmp_path / "credentials.json")
    service = CredentialService(EmptyEnvironment(), FailingKeyring(), file_store)

    storage = service.save(
        "openrouter",
        "secret-token",
        allow_plaintext_file=True,
    )

    assert storage == "file"
    assert service.load("openrouter") == "secret-token"


def test_working_keyring_is_preferred(tmp_path):
    keyring = WorkingKeyring()
    file_store = FileStore(tmp_path / "credentials.json")
    service = CredentialService(EmptyEnvironment(), keyring, file_store)

    assert service.save("openrouter", "secret-token") == "keyring"
    assert service.load("openrouter") == "secret-token"
    assert not file_store.path.exists()


@pytest.mark.parametrize(
    "provider",
    ["OpenRouter", "../openrouter", "openrouter\nmalicious", "", "a" * 65],
)
def test_invalid_provider_ids_are_rejected(provider):
    service = CredentialService(EmptyEnvironment(), WorkingKeyring(), FileStore())

    with pytest.raises(ValueError, match="Provider ID"):
        service.save(provider, "secret-token")


def test_empty_credentials_are_rejected():
    service = CredentialService(EmptyEnvironment(), WorkingKeyring(), FileStore())

    with pytest.raises(ValueError, match="must not be empty"):
        service.save("openrouter", "   ")
