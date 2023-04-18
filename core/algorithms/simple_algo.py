from abc import ABC

from core.algorithms import BaseAlgo
from core.data_set import DataSet
from core.signal import Signal
from core.signal_type import SignalType


class SimpleAlgo(BaseAlgo, ABC):
    def process(self, data_set: DataSet):
        yield Signal(SignalType.LE, __name__, data_set.quote)
