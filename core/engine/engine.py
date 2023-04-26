import asyncio
import logging
from abc import ABC
from typing import final

from core.broker_client import BrokerClient
from core.common.chart_settings import ChartSettings
from core.common.data_set import DataSet
from core.common.start_mode import StartMode
from core.config import start_mode, data_polling_interval_in_milliseconds
from core.data_services.bar_data_service import BarDataService
from core.data_services.option_chain_data_service import OptionChainDataService
from core.data_services.quote_data_service import QuoteDataService
from core.engine import BaseEngine


@final
class Engine(BaseEngine, ABC):
    def __init__(self, tickers: list[str], proxy_broker_client: BrokerClient, chart_settings: ChartSettings,
                 algorithm_list: list[any]):
        self.logger = logging.getLogger(__name__)
        self.start_mode = start_mode

        self.tickers = tickers
        self.proxy_broker_client = proxy_broker_client
        self.chart_settings = chart_settings
        self.algorithm_list: list[any] = algorithm_list

        if self.start_mode == StartMode.PULLING:
            self.quote_data_service: QuoteDataService = QuoteDataService(self.proxy_broker_client, self.tickers)
            self.option_chain_data_service: OptionChainDataService = OptionChainDataService(self.proxy_broker_client,
                                                                                            self.tickers)
        else:
            self.streamingService = None

        self.bar_data_service = BarDataService(self.proxy_broker_client, self.tickers, self.chart_settings)

    async def start(self):
        self.logger.info('Engine has started!')
        try:
            tasks = set()
            tasks.add(asyncio.create_task(self._run_data_collector()))
            tasks.add(asyncio.create_task(self._run_data_processor()))

            await asyncio.gather(*tasks)
        finally:
            self.logger.info('Engine has finished!')

    async def _run_data_collector(self):
        self.logger.info('Data collector has started!')
        try:
            tasks = set()
            #tasks.add(asyncio.create_task(self.bar_data_service.run(self.chart_settings.frequency * 60 * 1000)))

            # Pulling mode
            if self.start_mode == StartMode.PULLING:
                tasks.add(asyncio.create_task(self.quote_data_service.run(data_polling_interval_in_milliseconds)))
                # tasks.add(asyncio.create_task(self.option_chain_data_service.run(data_polling_interval_in_milliseconds)))
            else:  # Pushing mode
                tasks.add(asyncio.create_task(self.streaming_data_service.start()))

            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            self.logger.warning('Data collector was interrupted by user!')
        finally:
            self.logger.info('Data collector has stopped!')

    async def _run_data_processor(self):
        self.logger.info('Data processor has started!')
        try:
            async def process():
                last_quote_update_time = None
                last_option_chain_update_time = None
                last_bar_update_time = None

                while True:
                    # Get data from queue
                    is_quote_updated = last_quote_update_time != self.quote_data_service.last_update_time
                    is_option_chain_updated = last_option_chain_update_time != self.option_chain_data_service.last_update_time
                    is_bar_updated = last_bar_update_time != self.bar_data_service.last_update_time

                    data_set = DataSet()
                    if is_quote_updated:
                        data_set.quotes = self.quote_data_service.latest_data

                    if is_option_chain_updated:
                        data_set.option_chains = self.option_chain_data_service.latest_data

                    if is_bar_updated:
                        data_set.bars = self.bar_data_service.latest_data

                    if data_set.has_data():
                        # Pass the data set to the algo to process
                        self.notify(data_set)

                    await asyncio.sleep(0.1)

            await asyncio.create_task(process())
        except asyncio.CancelledError:
            self.logger.warning('Data processor was interrupted by user!')
        finally:
            self.logger.info('Data processor has stopped!')
