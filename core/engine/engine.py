import asyncio
import logging
from abc import ABC
from typing import final

from core.algorithms import BaseAlgo
from core.data_queue import DataQueue
from core.engine import BaseEngine
from core.signal_listener import SignalListener


@final
class Engine(BaseEngine, ABC):
    def __init__(self,
                 data_queue: DataQueue,
                 algorithm_list: list[BaseAlgo],
                 signal_listener_list: list[SignalListener]):
        self.logger = logging.getLogger(__name__)
        self.data_queue: DataQueue = data_queue
        self.algorithm_list: list[BaseAlgo] = algorithm_list
        self.signal_listener_list: list[SignalListener] = signal_listener_list

    async def start(self):
        self.logger.info('Engine has started!')
        try:
            tasks = set()

            tasks.add(asyncio.create_task(self._run_data_collector()))
            tasks.add(asyncio.create_task(self._run_data_processor()))

            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error('Engine was terminated with error: ' + str(e))
        finally:
            self.logger.info('Engine has finished!')

    async def _run_data_collector(self):
        self.logger.info('Data collector has started!')
        try:
            await asyncio.create_task(self.data_queue.acquire_latest_data())
        except asyncio.CancelledError:
            self.logger.warning('Data collector was interrupted by user!')
        finally:
            self.logger.info('Data collector has stopped!')

    async def _run_data_processor(self):
        self.logger.info('Data processor has started!')
        try:
            async def process():
                while True:
                    # Get data from queue
                    data_set_list = await self.data_queue.get_latest_data()

                    for data_set in data_set_list:
                        # Pass the data set to the algo to process
                        for algorithm in self.algorithm_list:
                            signal_generator = algorithm.process(data_set)

                            # Notify the signal listener
                            for signal in signal_generator:
                                for signal_listener in self.signal_listener_list:
                                    signal_listener.handle_signal(signal)

            await asyncio.create_task(process())
        except asyncio.CancelledError:
            self.logger.warning('Data processor was interrupted by user!')
        finally:
            self.logger.info('Data processor has stopped!')
