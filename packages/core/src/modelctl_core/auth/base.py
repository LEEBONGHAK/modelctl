from abc import ABC
from abc import abstractmethod


class CredentialStore(ABC):

    @abstractmethod
    def save(
        self,
        service: str,
        key: str,
        secret: str,
    ) -> None:
        ...

    @abstractmethod
    def load(
        self,
        service: str,
        key: str,
    ) -> str | None:
        ...

    @abstractmethod
    def delete(
        self,
        service: str,
        key: str,
    ) -> None:
        ...