from abc import abstractmethod

from core.signal import Signal


class SignalListener:
    @abstractmethod
    def handle_signal(self, signal: Signal):
        pass
