class OpenRouterProvider(Provider):
    id = "openrouter"

    display_name = "OpenRouter"

    def list_models(
        self,
        credential,
    ):

        client = OpenRouterClient(credential)

        raw = client.get_models()

        mapper = OpenRouterMapper()

        return [mapper.map(m) for m in raw]
