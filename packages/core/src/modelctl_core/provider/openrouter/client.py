import httpx


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, credential):

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {credential.api_key}",
                "HTTP-Referer": "https://github.com/modelctl/modelctl",
                "X-Title": "modelctl",
            },
            timeout=30,
        )

    def get_models(self):

        response = self.client.get("/models")

        response.raise_for_status()

        return response.json()["data"]
