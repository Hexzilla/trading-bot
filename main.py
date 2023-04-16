import asyncio
import logging

from core.engine import Engine
from logging_config import config

if __name__ == '__main__':
    config()
    logger = logging.getLogger()

    logger.info('Application started!')

    engine = Engine()
    asyncio.run(engine.start())

    logger.info('Application finished!')