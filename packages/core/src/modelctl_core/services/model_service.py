from modelctl_core.repository.model_repository import ModelRepository


class ModelService:

    def __init__(
        self,
        repository: ModelRepository,
        provider,
        mapper,
    ):
        self.repository = repository
        self.provider = provider
        self.mapper = mapper

    def sync(self):

        raw_models = self.provider.list_models()

        models = [
            self.mapper.map(m)
            for m in raw_models
        ]

        self.repository.delete_all()

        self.repository.save_many(models)

        return len(models)

    def list(self):
        return self.repository.list()