from __future__ import annotations

import httpx


class GoogleModelsClient:
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    PAGE_SIZE = 1000
    MAX_PAGES = 100

    def __init__(self, credential) -> None:
        api_key = credential.api_key
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("Google Gemini API credential is missing.")
        self.api_key = api_key.strip()

    def get_models(self) -> list[dict[str, object]]:
        timeout = httpx.Timeout(30.0, connect=10.0)
        models: list[dict[str, object]] = []
        page_token: str | None = None
        seen_tokens: set[str] = set()

        with httpx.Client(
            base_url=self.BASE_URL,
            headers={"x-goog-api-key": self.api_key},
            timeout=timeout,
            follow_redirects=False,
        ) as client:
            for _ in range(self.MAX_PAGES):
                params: dict[str, str | int] = {"pageSize": self.PAGE_SIZE}
                if page_token is not None:
                    params["pageToken"] = page_token

                response = client.get("/models", params=params)
                response.raise_for_status()
                payload = response.json()

                if not isinstance(payload, dict) or not isinstance(
                    payload.get("models"), list
                ):
                    raise ValueError("Google returned an invalid model response.")

                models.extend(
                    item for item in payload["models"] if isinstance(item, dict)
                )

                next_token = payload.get("nextPageToken")
                if next_token in (None, ""):
                    return models
                if not isinstance(next_token, str):
                    raise ValueError("Google returned invalid pagination metadata.")
                if next_token in seen_tokens:
                    raise ValueError("Google repeated a model pagination token.")

                seen_tokens.add(next_token)
                page_token = next_token

        raise ValueError("Google model pagination exceeded the safety limit.")
