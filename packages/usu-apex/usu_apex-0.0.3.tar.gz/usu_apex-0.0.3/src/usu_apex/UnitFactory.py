from abc import ABC, abstractmethod


class UnitFactory(ABC):

    @abstractmethod
    def giveDict(self):
        pass