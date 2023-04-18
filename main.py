import asyncio
import logging
import os
import time

from brokers.tda.broker_client import BrokerClient
from brokers.tda.order_handlers.tda_order_processor import TdaOrderProcessor
from core.algorithms.simple_algo import SimpleAlgo
from core.data_queue import DataQueue
from core.engine.engine import Engine
from logging_config import config_logger

config_logger()
logger = logging.getLogger()

loop = asyncio.get_event_loop()


async def main():
    try:
        logger.info('Application started!')

        seconds_per_day = 24 * 60 * 60

        tda_api_keys = [os.getenv('TDA_API_KEY')]
        tickers = ['SPY', 'TSLA', 'AAPL']
        realtime_trading = True
        num_data_days = 3
        data_polling_freq_in_seconds = 0.6
        end_time_in_seconds = time.time() if realtime_trading else time.time() - seconds_per_day * 90
        start_time_in_seconds = end_time_in_seconds - seconds_per_day * num_data_days

        tasks = set()
        broker_client_list = list()
        signal_listener_list = list()
        algorithm_list = list()

        # TDA clients
        for tda_api_key in tda_api_keys:
            broker_client = BrokerClient(tda_api_key)
            broker_client_list.append(broker_client)

            tda_order_processor = TdaOrderProcessor(broker_client)
            signal_listener_list.append(tda_order_processor)

        # Shared data queue among the broker clients
        data_queue = DataQueue(broker_client_list[0],
                               tickers,
                               data_polling_freq_in_seconds,
                               start_time_in_seconds,
                               end_time_in_seconds)

        # Algorithms
        algorithm_list.append(SimpleAlgo())

        # Main engine
        engine = Engine(data_queue, algorithm_list, signal_listener_list)

        # Create task and wait for the engine task to finish
        tasks.add(asyncio.create_task(engine.start()))
        await asyncio.gather(*tasks)

    except Exception as e:
        logger.error('Engine was terminated with error: ' + str(e))
    finally:
        logger.info('Application finished!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('User terminated the application!')
