from abc import ABC
from abc import abstractmethod

from modelctl_core.auth.types import Credential
from modelctl_core.models.universal_model import UniversalModel


class Provider(ABC):
    id: str
    display_name: str

    @abstractmethod
    def list_models(
        self,
        credential: Credential,
    ) -> list[UniversalModel]:
        raise NotImplementedError
