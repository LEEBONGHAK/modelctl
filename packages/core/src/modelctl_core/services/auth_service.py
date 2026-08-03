from modelctl_core.auth.service import CredentialService


class AuthService:
    def __init__(self, credentials: CredentialService | None = None) -> None:
        self.credentials = credentials or CredentialService()

    def save(
        self,
        provider: str,
        token: str,
        *,
        allow_plaintext_file: bool = False,
    ) -> str:
        return self.credentials.save(
            provider,
            token,
            allow_plaintext_file=allow_plaintext_file,
        )

    def load(self, provider: str) -> str | None:
        return self.credentials.load(provider)

    def delete(self, provider: str) -> None:
        self.credentials.delete(provider)
