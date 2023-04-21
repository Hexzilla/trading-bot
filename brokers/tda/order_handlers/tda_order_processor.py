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
        self.account_id = None
        
    def get_client(self) -> Client:
        return self.broker_client._get_client()

    def handle_signal(self, signal: Signal):
        self.logger.warning('Caught algo signal: ' + signal.__str__())

        account_id = self.get_account_id()
        if account_id is None:
            self.logger.error('Can not get account_id')
            return

        if signal.signal_type == SignalType.LE:
            self.place_order(account_id, 'buy', signal.data.symbol)
        elif signal.signal_type == SignalType.SE:
            self.place_order(account_id, 'sell', signal.data.symbol)

    def get_account_id(self):
        if self.account_id:
            return self.account_id

        tda_client = self.get_client()
        response = tda_client.get_accounts(fields=[tda_client.Account.Fields.POSITIONS])
        if response.status_code == 200:
            positions = response.json()
            if len(positions) > 0:
                position = positions[0]['securitiesAccount']
                self.account_id = position['accountId']

        return self.account_id

    def place_order(self, account_id: str, order_type: str, ticker: str):
        tda_client: Client = self.get_client()

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

        tda_client: Client = self.get_client()
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
        tda_client: Client = self.get_client()
        tda_client.cancel_order(order_id, account_id)

    def get_order(self, account_id: str, order_id: str):
        tda_client: Client = self.get_client()
        return tda_client.get_order(order_id, account_id)

    def get_orders(self, account_id: str = None):
        tda_client: Client = self.get_client()
        return tda_client.get_orders_by_path(account_id)
