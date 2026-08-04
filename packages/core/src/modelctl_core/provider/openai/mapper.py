from modelctl_core.models.universal_model import UniversalModel


class OpenAIModelMapper:
    _CODING_PREFIXES = ("gpt-", "o1", "o3", "o4", "codex-")
    _NON_CODING_MARKERS = (
        "audio",
        "computer-use",
        "deep-research",
        "embedding",
        "image",
        "moderation",
        "realtime",
        "search",
        "sora",
        "transcribe",
        "tts",
    )

    def supports_coding(self, raw: dict[str, object]) -> bool:
        model_id = raw.get("id")
        if not isinstance(model_id, str) or not model_id:
            return False

        normalized = model_id.lower()
        if normalized.startswith("ft:"):
            return False
        if any(marker in normalized for marker in self._NON_CODING_MARKERS):
            return False

        return normalized.startswith(self._CODING_PREFIXES)

    def map(self, raw: dict[str, object]) -> UniversalModel:
        model_id = raw.get("id")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError("OpenAI model response is missing an ID.")

        normalized = model_id.lower()
        return UniversalModel(
            provider="openai",
            model_id=model_id,
            name=model_id,
            context_length=0,
            supports_vision=False,
            supports_tools=True,
            supports_reasoning=(
                normalized.startswith(("o1", "o3", "o4", "gpt-5"))
                or "codex" in normalized
            ),
        )
