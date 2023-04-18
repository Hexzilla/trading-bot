import asyncio
from asyncio import Queue

from core.broker_client import BaseBrokerClient


class DataQueue:
    def __init__(self, broker_client: BaseBrokerClient, tickers: list[str], data_polling_freq,
                 start_time_in_seconds, end_time_in_seconds):
        self.broker_client = broker_client
        self.tickers = tickers
        self.data_queue = Queue(1)

        assert tickers is not None or len(tickers) > 0, 'Invalid ticker list'
        assert 0.1 <= data_polling_freq <= 1.0, 'data_polling_freq must be [1, 5]'

        self.data_polling_freq = data_polling_freq
        self.start_time = start_time_in_seconds * 1000
        self.end_time = end_time_in_seconds * 1000

    async def acquire_latest_data(self):
        while True:
            # Get latest data
            data_set_generator = self.broker_client.get_data(self.tickers)

            data_set_list = list()
            for data_set in data_set_generator:
                data_set_list.append(data_set)

            # If queue is full, replace the old data with the latest data set list
            if self.data_queue.full():
                self.data_queue.get_nowait()

            await self.data_queue.put(data_set_list)

            # Sleep
            await asyncio.sleep(self.data_polling_freq)

            # Update start/end time
            self.end_time = self.end_time + self.data_polling_freq * 1000
            self.start_time = self.start_time + self.data_polling_freq * 1000

    async def get_latest_data(self) -> list:
        return await self.data_queue.get()
