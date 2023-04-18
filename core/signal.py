from core.algorithms import BaseAlgo
from core.signal_type import SignalType


class Signal:
    def __init__(self, signal_type: SignalType, algo_name: str, data: any):
        self.signal_type = signal_type
        self.algo_name = algo_name
        self.data = data

    def __str__(self):
        return 'Signal type: ' + str(self.signal_type.value) + \
               ' - Algo: ' + self.algo_name + \
               ' - Data: ' + str(self.data)
