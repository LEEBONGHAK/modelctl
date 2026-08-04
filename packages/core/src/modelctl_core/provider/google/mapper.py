from modelctl_core.models.universal_model import UniversalModel


class GoogleModelMapper:
    GENERATE_CONTENT = "generateContent"

    def supports_generation(self, raw: dict[str, object]) -> bool:
        methods = raw.get("supportedGenerationMethods")
        return (
            isinstance(methods, list)
            and self.GENERATE_CONTENT in methods
        )

    def map(self, raw: dict[str, object]) -> UniversalModel:
        resource_name = raw.get("name")
        display_name = raw.get("displayName")
        if not isinstance(resource_name, str) or not resource_name.startswith("models/"):
            raise ValueError("Google model response is missing a valid resource name.")
        model_id = resource_name.removeprefix("models/")
        if not model_id:
            raise ValueError("Google model response is missing a model ID.")
        if not isinstance(display_name, str) or not display_name:
            raise ValueError("Google model response is missing a display name.")

        context_length = raw.get("inputTokenLimit", 0)
        if not isinstance(context_length, int) or context_length < 0:
            context_length = 0

        return UniversalModel(
            provider="google",
            model_id=model_id,
            name=display_name,
            context_length=context_length,
            supports_vision=False,
            supports_tools=self.supports_generation(raw),
            supports_reasoning=raw.get("thinking") is True,
        )
