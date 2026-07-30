from modelctl.providers.openrouter import (
    OpenRouterProvider
)



PROVIDERS = {
    "openrouter": OpenRouterProvider,
}



def get_provider(name):
    provider = PROVIDERS.get(name)
    if provider is None:
        return None

    return provider()



def list_providers():
    return list(
        PROVIDERS.keys()
    )
