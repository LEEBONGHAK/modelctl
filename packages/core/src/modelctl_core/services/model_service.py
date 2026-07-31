from modelctl_core.repository.model_repository import ModelRepository


class ModelService:
    def __init__(
        self,
        repository: ModelRepository,
        provider_registry,
        credentials,
    ):
        self.repository = repository
        self.provider_registry = provider_registry
        self.credentials = credentials

    def sync(self, provider_name="openrouter"):
        provider = self.provider_registry.get(provider_name)

        token = self.credentials.load(provider_name)

        provider.authenticate(token)

        models = provider.list_models()

        self.repository.save_many(models)

        return len(models)

    def list(self):
        return self.repository.list()
