from modelctl.providers.base import Provider


class MockProvider(Provider):
    name = "mock"

    def validate(self):

        return True

    def list_models(self):

        return [{"id": "test-model"}]
