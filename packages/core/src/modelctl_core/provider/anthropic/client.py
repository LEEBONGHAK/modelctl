from __future__ import annotations

import httpx


class AnthropicClient:
    BASE_URL = "https://api.anthropic.com/v1"
    API_VERSION = "2023-06-01"
    PAGE_LIMIT = 1000
    MAX_PAGES = 100

    def __init__(self, credential) -> None:
        api_key = credential.api_key
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("Anthropic API credential is missing.")
        self.api_key = api_key.strip()

    def get_models(self) -> list[dict[str, object]]:
        timeout = httpx.Timeout(30.0, connect=10.0)
        models: list[dict[str, object]] = []
        after_id: str | None = None
        seen_cursors: set[str] = set()

        with httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": self.API_VERSION,
            },
            timeout=timeout,
            follow_redirects=False,
        ) as client:
            for _ in range(self.MAX_PAGES):
                params: dict[str, str | int] = {"limit": self.PAGE_LIMIT}
                if after_id is not None:
                    params["after_id"] = after_id

                response = client.get("/models", params=params)
                response.raise_for_status()
                payload = response.json()

                if not isinstance(payload, dict) or not isinstance(
                    payload.get("data"), list
                ):
                    raise ValueError("Anthropic returned an invalid model response.")

                models.extend(
                    item for item in payload["data"] if isinstance(item, dict)
                )

                has_more = payload.get("has_more")
                if has_more is False:
                    return models
                if has_more is not True:
                    raise ValueError("Anthropic returned invalid pagination metadata.")

                last_id = payload.get("last_id")
                if not isinstance(last_id, str) or not last_id:
                    raise ValueError("Anthropic omitted the next model cursor.")
                if last_id in seen_cursors:
                    raise ValueError("Anthropic repeated a model pagination cursor.")

                seen_cursors.add(last_id)
                after_id = last_id

        raise ValueError("Anthropic model pagination exceeded the safety limit.")
