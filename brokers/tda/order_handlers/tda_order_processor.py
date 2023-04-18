import logging

from brokers.tda.broker_client import BrokerClient
from core.order_handlers.order_processor import OrderProcessor
from core.signal import Signal


class TdaOrderProcessor(OrderProcessor):
    def __init__(self, broker_client: BrokerClient):
        super().__init__(broker_client)
        self.logger = logging.getLogger(__name__)

    def handle_signal(self, signal: Signal):
        self.logger.warning('Caught algo signal: ' + signal.__str__())

    def place_order(self, account_id: str, ticker: str):
        pass

    def replace_order(self, account_id: str, order_id: str):
        pass

    def cancel_order(self, account_id: str, order_id: str):
        pass

    def get_order(self, account_id: str, order_id: str):
        pass

    def get_orders(self, account_id: str = None):
        pass
