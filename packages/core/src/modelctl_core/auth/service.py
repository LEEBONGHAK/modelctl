class CredentialService:
    def __init__(self):

        self.backends = [
            EnvironmentStore(),
            KeyringStore(),
            FileStore(),
        ]

    def load(self, provider):

        for backend in self.backends:
            token = backend.load(
                "modelctl",
                provider,
            )

            if token:
                return token

        return None

    def save(self, provider, token):

        self.backends[1].save(
            "modelctl",
            provider,
            token,
        )
