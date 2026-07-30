import keyring

from modelctl_core.auth.base import CredentialStore


class KeyringStore(CredentialStore):

    def save(self, service, key, secret):

        keyring.set_password(
            service,
            key,
            secret,
        )

    def load(self, service, key):

        return keyring.get_password(
            service,
            key,
        )

    def delete(self, service, key):

        keyring.delete_password(
            service,
            key,
        )