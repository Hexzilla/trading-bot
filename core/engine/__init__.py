import asyncio
import logging


class Engine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.background_tasks = set()

    async def start(self):
        self.logger.info('Engine has started!')
        data_collector_task = asyncio.create_task(self.__run_data_collector())
        data_processor_task = asyncio.create_task(self.__run_data_processor())
        await asyncio.gather(data_collector_task, data_processor_task)
        self.logger.info('Engine has finished!')

    async def stop(self):
        self.logger.info('Engine is stopping...')
        self.logger.info('Engine has stopped!')
        pass

    async def __run_data_collector(self):
        self.logger.info('Data collector has started!')
        self.logger.info('Data collector has stopped!')
        await asyncio.sleep(1)
        pass

    async def __run_data_processor(self):
        self.logger.info('Data processor has started!')
        self.logger.info('Data processor has stopped!')
        await asyncio.sleep(1)
        pass
