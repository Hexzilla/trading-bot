from abc import ABC

from core.algorithms import Algo
from core.common.signal import Signal
from core.common.signal_type import SignalType


class SimpleAlgo(Algo, ABC):
    def update(self, data: any):
        signal = Signal(SignalType.LE, __name__, data)
        print('>>>>>>>>>>>>>Signal = ' + super()._observers.__str__())
        self.notify(signal)
