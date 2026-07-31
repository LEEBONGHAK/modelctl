class SelectionService:
    def __init__(
        self,
        registry,
        model_repository,
        selector,
    ):
        self.registry = registry
        self.repository = model_repository
        self.selector = selector

    def select_provider(self):

        providers = self.registry.list()

        return self.selector.select("Select Provider", [p.display_name for p in providers])

    def select_model(self, provider):
        models = self.repository.list_by_provider(provider)

        choices = []

        for model in models:
            prefix = "★ " if model.favorite else ""

            choices.append(prefix + model.model_id)

        return self.selector.select("Select Model", choices)
