from abc import abstractmethod

from core.common.subject import Subject


class BaseEngine(Subject):
    @abstractmethod
    async def start(self):
        pass


