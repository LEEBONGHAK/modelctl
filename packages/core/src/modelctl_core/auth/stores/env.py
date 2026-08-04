import os

from modelctl_core.auth.base import CredentialStore


_PROVIDER_ENV_ALIASES = {
    "anthropic": ("ANTHROPIC_API_KEY",),
    "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
}


class EnvironmentStore(CredentialStore):
    def save(self, *args):
        raise RuntimeError("Environment variables are read-only.")

    def load(self, service, key):
        env_name = f"{service}_{key}".upper().replace("-", "_")
        token = os.getenv(env_name)
        if token:
            return token

        for alias in _PROVIDER_ENV_ALIASES.get(key, ()):
            token = os.getenv(alias)
            if token:
                return token

        return None

    def delete(self, *args):
        pass
