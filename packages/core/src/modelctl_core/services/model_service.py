class ModelService:
    def __init__(
        self,
        repository,
        providers,
        credential_store,
    ):

        self.repository = repository

        self.providers = providers

        self.credential_store = credential_store

    def sync(
        self,
        provider_name="openrouter",
    ):

        provider = self.providers.get(provider_name)

        credential = self.credential_store.get(provider_name)

        models = provider.list_models(credential)

        self.repository.save_many(models)

        return len(models)

    def list(self):

        return self.repository.list()

    def search(
        self,
        keyword,
    ):

        return self.repository.search(keyword)

    def favorite(
        self,
        model_id,
        value=True,
    ):

        return self.repository.favorite(
            model_id,
            value,
        )

    def favorites(self):

        return self.repository.favorites()
