import asyncio
import logging
import os

from brokers.tda.db import db_account
from brokers.tda.broker_client import BrokerClient
from brokers.tda.order_handlers.tda_order_processor import TdaOrderProcessor
from core.algorithms.simple_algo import SimpleAlgo
from core.config import default_chart_settings
from core.engine.engine import Engine
from logging_config import config_logger

config_logger()
logger = logging.getLogger()

loop = asyncio.get_event_loop()


def update_account_info(broker_client):
    account_id = broker_client.get_account_id()
    if account_id:
        exist = db_account.select_by_user_id(account_id)
        if exist:
            db_account.update_account((account_id, True))
        else:
            db_account.insert_account((account_id, True))


async def main():
    tasks = set()
    broker_client_list = list()
    algorithm_list = list()

    try:
        logger.info('Application started!')

        tda_api_keys = [os.getenv('TDA_API_KEY')]
        tickers = ['SPY']

        # Algorithms
        simpleAlgo = SimpleAlgo()
        algorithm_list.append(simpleAlgo)

        # TDA clients
        for tda_api_key in tda_api_keys:
            broker_client = BrokerClient(tda_api_key)
            broker_client_list.append(broker_client)

            # Update account_info table
            update_account_info(broker_client)

            tda_order_processor = TdaOrderProcessor(broker_client)
            simpleAlgo.subscribe(tda_order_processor)

        # Main engine
        engine = Engine(tickers, broker_client_list[0], default_chart_settings, algorithm_list)

        for algo in algorithm_list:
            engine.subscribe(algo)

        # Create task and wait for the engine task to finish
        tasks.add(asyncio.create_task(engine.start()))
        await asyncio.gather(*tasks)

    finally:
        if engine is not None:
            engine.clear()

        for algo in algorithm_list:
            algo.clear()

        logger.info('Application finished!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('User terminated the application!')
