import getpass

import httpx

from modelctl.providers.base import Provider
from modelctl.services.credential import (
    set_secret,
    get_secret,
)


class OpenRouterProvider(Provider):

    name = "openrouter"


    BASE_URL = (
        "https://openrouter.ai/api/v1"
    )


    def login(self):

        """
        Store OpenRouter API Key.
        """

        key = getpass.getpass(
            "OpenRouter API Key: "
        )
        if not key:
            raise ValueError(
                    "API key cannot be empty"
            )

        set_secret(
            "openrouter",
            key,
        )


    def validate(self) -> bool:

        key = get_secret(
            "openrouter"
        )

        return key is not None



    def list_models(self):

        key = get_secret(
            "openrouter"
        )

        if not key:

            raise RuntimeError(
                "OpenRouter API key is not configured."
            )


        headers = {
            "Authorization":
                f"Bearer {key}"
        }


        response = httpx.get(
            f"{self.BASE_URL}/models",
            headers=headers,
            timeout=30,
        )


        response.raise_for_status()


        return response.json()["data"]
