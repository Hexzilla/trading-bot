import asyncio
import logging
import signal
from asyncio import Task, AbstractEventLoop


class Engine:
    def __init__(self):
        self.loop: AbstractEventLoop = None
        self.data_processor_task: Task = None
        self.data_collector_task: Task = None
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info('Engine has started!')

        self.loop = asyncio.get_event_loop()

        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGILL]:
            self.loop.add_signal_handler(sig, lambda: asyncio.create_task(self.__shutdown(signal.SIGTERM)))

        try:
            asyncio.ensure_future(self.__run_data_collector(), loop=self.loop)
            asyncio.ensure_future(self.__run_data_processor(), loop=self.loop)

            self.loop.run_forever()
        except Exception as e:
            self.logger.error('Engine was terminated with error: ' + str(e))
        finally:
            self.loop.close()
            self.logger.info('Engine has finished!')

    async def __shutdown(self, sig):
        print('caught {0}'.format(sig.name))
        tasks = [task for task in asyncio.all_tasks(self.loop) if task is not asyncio.current_task(self.loop)]
        list(map(lambda task: task.cancel(), tasks))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print('finished awaiting cancelled tasks, results: {0}'.format(results))
        self.loop.stop()

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
