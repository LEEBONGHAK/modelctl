from modelctl_core.models.universal_model import UniversalModel


class AnthropicMapper:
    def map(self, raw: dict[str, object]) -> UniversalModel:
        model_id = raw.get("id")
        display_name = raw.get("display_name")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError("Anthropic model response is missing an ID.")
        if not isinstance(display_name, str) or not display_name:
            raise ValueError("Anthropic model response is missing a display name.")

        context_length = raw.get("max_input_tokens", 0)
        if not isinstance(context_length, int) or context_length < 0:
            context_length = 0

        capabilities = raw.get("capabilities")
        if not isinstance(capabilities, dict):
            capabilities = {}

        return UniversalModel(
            provider="anthropic",
            model_id=model_id,
            name=display_name,
            context_length=context_length,
            supports_vision=self._supported(capabilities, "image_input"),
            supports_tools=True,
            supports_reasoning=self._supported(capabilities, "thinking"),
        )

    @staticmethod
    def _supported(capabilities: dict[str, object], name: str) -> bool:
        capability = capabilities.get(name)
        return isinstance(capability, dict) and capability.get("supported") is True
