import asyncio
from abc import ABC
from typing import final

from core.engine import BaseEngine


@final
class Engine(BaseEngine, ABC):

    async def __run_data_collector(self):
        self.logger.info('Data collector has started!')
        try:
            await asyncio.sleep(1, loop=self.loop)
        except asyncio.CancelledError:
            self.logger.warning('Data collector was interrupted by user!')
        finally:
            self.logger.info('Data collector has stopped!')

    async def __run_data_processor(self):
        self.logger.info('Data processor has started!')
        try:
            await asyncio.sleep(10, loop=self.loop)
        except asyncio.CancelledError:
            self.logger.warning('Data processor was interrupted by user!')
        finally:
            self.logger.info('Data processor has stopped!')
