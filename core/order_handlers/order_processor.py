from abc import ABC, abstractmethod

from brokers.tda.broker_client import BrokerClient
from core.common.observer import Observer


class OrderProcessor(Observer, ABC):
    def __init__(self, broker_client: BrokerClient):
        self.broker_client = broker_client

    @abstractmethod
    def place_order(self, account_id: str, ticker: str):
        pass

    @abstractmethod
    def replace_order(self, account_id: str, order_id: str):
        pass

    @abstractmethod
    def cancel_order(self, account_id: str, order_id: str):
        pass

    @abstractmethod
    def get_order(self, account_id: str, order_id: str):
        pass

    @abstractmethod
    def get_orders(self, account_id: str = None):
        pass
