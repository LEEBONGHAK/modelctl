import os

from modelctl_core.auth.base import CredentialStore


class EnvironmentStore(CredentialStore):
    def save(self, *args):

        raise RuntimeError("Environment variables are read-only.")

    def load(self, service, key):

        env_name = f"{service}_{key}".upper().replace("-", "_")

        return os.getenv(env_name)

    def delete(self, *args):

        pass
