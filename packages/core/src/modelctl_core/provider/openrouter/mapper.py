import json

from modelctl_core.models.universal_model import UniversalModel


class OpenRouterMapper:
    def map(self, raw):

        return UniversalModel(
            provider="openrouter",
            model_id=raw["id"],
            display_name=raw["name"],
            context_length=raw["context_length"],
            prompt_price=float(raw["pricing"]["prompt"]),
            completion_price=float(raw["pricing"]["completion"]),
            supports_tools=True,
            metadata=json.dumps(raw),
        )
