from modelctl_core.auth.types import Credential


class ModelService:
    def __init__(
        self,
        repository,
        provider_registry,
        credentials,
    ) -> None:
        self.repository = repository
        self.providers = provider_registry
        self.credentials = credentials

    def sync(self, provider_id: str = "openrouter") -> int:
        try:
            provider = self.providers.get(provider_id)
        except KeyError as error:
            raise ValueError(f"Unknown provider: {provider_id}") from error

        api_key = self.credentials.load(provider_id)
        if not api_key:
            raise RuntimeError(
                f"No credential found for {provider_id}. "
                f"Run: modelctl auth login {provider_id}"
            )

        models = provider.list_models(Credential(api_key=api_key))
        self.repository.save_many(models)
        return len(models)

    def list(self):
        return self.repository.list()

    def search(self, keyword):
        return self.repository.search(keyword)

    def favorite(self, model_id, value=True):
        return self.repository.favorite(model_id, value)

    def favorites(self):
        return self.repository.favorites()
