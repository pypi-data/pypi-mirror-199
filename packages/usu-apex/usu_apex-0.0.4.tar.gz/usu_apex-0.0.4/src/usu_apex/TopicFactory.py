from abc import ABC, abstractmethod


class TopicFactory(ABC):

    @abstractmethod
    def giveInfo(self):
        pass

    def Bonus(self, info):
        pass