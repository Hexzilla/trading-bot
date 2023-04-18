from abc import abstractmethod


class BaseEngine:
    @abstractmethod
    async def start(self):
        pass


