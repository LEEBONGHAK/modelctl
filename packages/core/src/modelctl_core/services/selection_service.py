class SelectionService:
    def __init__(self, registry, model_repository, selector):
        self.registry = registry
        self.repository = model_repository
        self.selector = selector

    def select_provider(self):
        providers = self.registry.list()
        choices = [provider.display_name for provider in providers]
        selected = self.selector.select("Select Provider", choices)

        if not selected:
            return None

        return next(
            provider.id
            for provider in providers
            if provider.display_name == selected
        )

    def select_model(self, provider_id):
        models = self.repository.list_by_provider(provider_id)
        choices = []

        for model in models:
            prefix = "★ " if model.favorite else ""
            choices.append(prefix + model.model_id)

        selected = self.selector.select("Select Model", choices)
        if not selected:
            return None

        return selected.removeprefix("★ ")
