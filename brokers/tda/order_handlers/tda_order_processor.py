import logging

from tda.client import Client
from tda.orders.common import Session, Duration
from tda.orders.equities import equity_buy_market, equity_sell_market

from brokers.tda.broker_client import BrokerClient
from core.order_handlers.order_processor import OrderProcessor
from core.signal import Signal
from core.signal_type import SignalType


class TdaOrderProcessor(OrderProcessor):
    def __init__(self, broker_client: BrokerClient):
        super().__init__(broker_client)
        self.logger = logging.getLogger(__name__)

    def handle_signal(self, signal: Signal):
        self.logger.warning('Caught algo signal: ' + signal.__str__())
        if signal.signal_type == SignalType.LE:
            account_id = self.get_account_id();
            self.place_order(account_id, 'buy', signal.data.symbol)
            pass
        elif signal.signal_type == SignalType.SE:
            account_id = self.get_account_id();
            self.place_order(account_id, 'sell', signal.data.symbol)
            pass

    def get_account_id(self):
        tda_client: Client = self.broker_client._get_client()

        positions = tda_client.get_accounts(fields=[tda_client.Account.Fields.POSITIONS])
        position = positions.json()[0]['securitiesAccount']
        return position['account_id']

    def place_order(self, account_id: str, order_type: str, ticker: str):
        tda_client: Client = self.broker_client._get_client()

        # order_type = 'buy'
        quantity = 10000000

        if order_type == 'buy':
            order_spec = equity_buy_market(ticker, quantity).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            result = tda_client.place_order(account_id, order_spec)
            self.logger.warning('Buy result: ' + result.__str__())

        if order_type == 'sell':
            order_spec = equity_sell_market(ticker, quantity).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            result = tda_client.place_order(account_id, order_spec)
            self.logger.warning('Sell result: ' + result.__str__())

    def replace_order(self, account_id: str, order_id: str):
        order = self.get_order(account_id, order_id)
        if order is None: return

        tda_client: Client = self.broker_client._get_client()
        order_type = 'buy'
        shares = 1
        ticker = ''

        if order_type == 'buy':
            order_spec = equity_buy_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            tda_client.replace_order(account_id, order_id, order_spec)

        if order_type == 'sell':
            order_spec = equity_sell_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            tda_client.replace_order(account_id, order_id, order_spec)

    def cancel_order(self, account_id: str, order_id: str):
        tda_client: Client = self.broker_client._get_client()
        tda_client.cancel_order(order_id, account_id)

    def get_order(self, account_id: str, order_id: str):
        tda_client: Client = self.broker_client._get_client()
        return tda_client.get_order(order_id, account_id)

    def get_orders(self, account_id: str = None):
        tda_client: Client = self.broker_client._get_client()
        return tda_client.get_orders_by_path(account_id)
