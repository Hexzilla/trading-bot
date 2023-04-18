import logging

from tda.client import Client
from tda.orders.common import Session, Duration
from tda.orders.equities import equity_buy_market, equity_sell_market

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
        tda_client: Client = self.broker_client._get_client()

        order_type = 'buy'
        shares = 1

        if order_type == 'buy':
            order_spec = equity_buy_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            tda_client.place_order(account_id, order_spec)

        if order_type == 'sell':
            order_spec = equity_sell_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            tda_client.place_order(account_id, order_spec)

    def replace_order(self, account_id: str, order_id: str):
        pass

    def cancel_order(self, account_id: str, order_id: str):
        pass

    def get_order(self, account_id: str, order_id: str):
        pass

    def get_orders(self, account_id: str = None):
        pass
