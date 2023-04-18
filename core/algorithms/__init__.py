from abc import abstractmethod

from core.data_set import DataSet


class BaseAlgo:
    @abstractmethod
    async def process(self, data_set: DataSet):
        yield
