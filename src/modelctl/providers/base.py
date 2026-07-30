from abc import ABC, abstractmethod


class Provider(ABC):
    """
    Base interface for AI model providers.

    Examples:
    - OpenRouter
    - OpenAI
    - Anthropic
    - Ollama
    """

    name: str


    def login(self):
        """
        Optional authentication flow.

        Providers without authentication
        can leave this unimplemented.
        """

        raise NotImplementedError(
            f"{self.name} does not support login."
        )


    def logout(self):
        """
        Optional logout flow.
        """

        raise NotImplementedError(
            f"{self.name} does not support logout."
        )


    @abstractmethod
    def validate(self) -> bool:
        """
        Validate provider configuration.
        """

        pass


    @abstractmethod
    def list_models(self):
        """
        Return available models.
        """

        pass
