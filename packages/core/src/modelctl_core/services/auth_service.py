import keyring


class AuthService:
    SERVICE = "modelctl"

    def save(
        self,
        provider,
        token,
    ):

        keyring.set_password(
            self.SERVICE,
            provider,
            token,
        )

    def load(
        self,
        provider,
    ):

        return keyring.get_password(
            self.SERVICE,
            provider,
        )
