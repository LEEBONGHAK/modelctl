class ModelSelector:
    def __init__(self, repository):
        self.repository = repository

    def choices(self):
        favorites = self.repository.favorite_models()
        recent = self.repository.recent()
        models = self.repository.list()

        return {
            "favorites": favorites,
            "recent": recent,
            "all": models,
        }
