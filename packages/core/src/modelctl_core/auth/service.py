from modelctl_core.auth.stores.env import EnvironmentStore
from modelctl_core.auth.stores.file import FileStore
from modelctl_core.auth.stores.keyring import KeyringStore


class CredentialService:
    def __init__(self):
        self.backends = [
            EnvironmentStore(),
            KeyringStore(),
            FileStore(),
        ]

    def load(self, provider):
        for backend in self.backends:
            token = backend.load("modelctl", provider)
            if token:
                return token

        return None

    def save(self, provider, token):
        try:
            self.backends[1].save("modelctl", provider, token)
        except Exception:
            self.backends[2].save("modelctl", provider, token)
