from abc import ABC, abstractmethod


class Launcher(ABC):

    @abstractmethod
    def run(self,model):
        