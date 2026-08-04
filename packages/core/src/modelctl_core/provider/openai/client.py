from __future__ import annotations

import httpx


class OpenAIModelsClient:
    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, credential) -> None:
        api_key = credential.api_key
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("OpenAI API credential is missing.")
        self.api_key = api_key.strip()

    def get_models(self) -> list[dict[str, object]]:
        timeout = httpx.Timeout(30.0, connect=10.0)

        with httpx.Client(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=timeout,
            follow_redirects=False,
        ) as client:
            response = client.get("/models")
            response.raise_for_status()
            payload = response.json()

        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("OpenAI returned an invalid model response.")

        return [item for item in payload["data"] if isinstance(item, dict)]
