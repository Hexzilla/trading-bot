import threading

from core.bars import Bars
from core.quote import Quote


class BaseAlgo:
    def __init__(self):
        self.bars = None
        self.quote = None
        self.lock = threading.Lock()

    async def execute(self, bars: Bars, quote: Quote):
        with self.lock:
            self.bars = bars
            self.quote = quote

        pass
