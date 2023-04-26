import logging
from abc import ABC

from tda.client import Client
from tda.orders.common import Session, Duration
from tda.orders.equities import equity_buy_market, equity_sell_market

from brokers.tda.broker_client import BrokerClient
from core.order_handlers.order_processor import OrderProcessor


class TdaOrderProcessor(OrderProcessor, ABC):
    def __init__(self, broker_client: BrokerClient):
        super().__init__(broker_client)
        self.logger = logging.getLogger(__name__)
        self.tda_client = self.broker_client.get_client()
        self.account_id = None

    def get_account_id(self):
        if self.account_id:
            return self.account_id

        response = self.tda_client.get_accounts(fields=[self.tda_client.Account.Fields.POSITIONS])
        if response.status_code == 200:
            positions = response.json()
            if len(positions) > 0:
                position = positions[0]['securitiesAccount']
                self.account_id = position['accountId']

        return self.account_id

    def update(self, data: any):
        print('Caught algo signal: ' + str(data))

    def place_order(self, account_id: str, ticker: str):
        account_id = self.get_account_id()
        if account_id is None:
            self.logger.error('Can not get account_id')
            return

        orders = self.get_orders(account_id)
        self.logger.warning('orders: ' + orders.__str__())

        """
        if signal.signal_type == SignalType.LE:
            self.place_order(account_id, 'buy', signal.data.symbol)
        elif signal.signal_type == SignalType.SE:
            self.place_order(account_id, 'sell', signal.data.symbol)
        """

    def place_order(self, account_id: str, order_type: str, ticker: str):
        # order_type = 'buy'
        quantity = 100000000000

        if order_type == 'buy':
            order_spec = equity_buy_market(ticker, quantity).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            result = self.tda_client.place_order(account_id, order_spec)
            self.logger.warning('Buy result: ' + result.__str__())

        if order_type == 'sell':
            order_spec = equity_sell_market(ticker, quantity).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            result = self.tda_client.place_order(account_id, order_spec)
            self.logger.warning('Sell result: ' + result.__str__())

    def replace_order(self, account_id: str, order_id: str):
        order = self.get_order(account_id, order_id)
        if order is None: return

        order_type = 'buy'
        shares = 1
        ticker = ''

        if order_type == 'buy':
            order_spec = equity_buy_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            self.tda_client.replace_order(account_id, order_id, order_spec)

        if order_type == 'sell':
            order_spec = equity_sell_market(ticker, shares).set_session(
                Session.NORMAL).set_duration(Duration.DAY).build()
            self.tda_client.replace_order(account_id, order_id, order_spec)

    def cancel_order(self, account_id: str, order_id: str):
        self.tda_client.cancel_order(order_id, account_id)

    def get_order(self, account_id: str, order_id: str):
        return self.tda_client.get_order(order_id, account_id)

    def get_orders(self, account_id: str = None):
        return self.tda_client.get_orders_by_path(account_id)
