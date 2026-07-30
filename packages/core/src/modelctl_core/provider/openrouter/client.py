import httpx


class OpenRouterClient:

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key):

        self.api_key = api_key

    def get_models(self):

        response = httpx.get(

            f"{self.BASE_URL}/models",

            headers={

                "Authorization":
                    f"Bearer {self.api_key}"

            },

            timeout=30,

        )

        response.raise_for_status()

        return response.json()["data"]