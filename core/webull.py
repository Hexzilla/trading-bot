import json
import os
import pickle
from webull import paper_webull
from brokers.tda.db import db_account, db_account_order

_email = 'thegreatone150@gmail.com'
_password = 'Tank2013!'
_deviceId = "72b0c5e07699488580fb5a30b9a4ecdc"
_regionId = 1


class paper_webull_wrapper(paper_webull):
    def set_did(self, did):
        self._set_did(did)

    def set_region_code(self, region_code):
        self._region_code = region_code

    def account_id(self):
        return self._account_id

    def login_with_email(self, email, password):
        result = self.login(email, password, 'Windows Chrome', save_token=True)
        return 'accessToken' in result

    def login_with_credentials(self, path=None):
        filename = 'webull_credentials.json'
        if path:
            filename = os.path.join(path, filename)

        if not os.path.isfile(filename):
            return None

        with open(filename, 'rb') as fh:
            credential_data = pickle.load(fh)

        self._refresh_token = credential_data['refreshToken']
        self._access_token = credential_data['accessToken']
        self._token_expire = credential_data['tokenExpireTime']
        self._uuid = credential_data['uuid']

        result = self.refresh_login(save_token=True)
        return 'accessToken' in result

    def place_buy_order(self, stock, price, quant):
        return self.place_order(stock=stock, price=price, action='BUY', quant=quant)

    def place_sell_order(self, stock, price, quant):
        return self.place_order(stock=stock, price=price, action='SELL', quant=quant)

    def update_current_orders(self):
        # Get standing orders
        orders = self.get_current_orders()
        if len(orders) > 0:
            for order in orders:
                # db_account_order.insert_account_order()
                pass


def create_webull():
    wb = paper_webull_wrapper()
    wb.set_did(_deviceId)
    wb.set_region_code(_regionId)

    result = wb.login_with_credentials()
    if not result:
        result = wb.login_with_email(_email, _password)

    if result:
        account_id = wb.account_id()
        db_account.upsert_account((str(account_id), True))
        return wb

    return None


def test_webull(logger):
    wb = create_webull()
    if wb is None:
        logger.error("Failed to login webull!")
        return

    # Authorize trade, must be done before trade action
    # wb.get_trade_token('123456')

    # Get standing orders
    # orders = wb.get_current_orders()
    # print(orders)

    # Place order - buy
    # result = wb.place_buy_order(stock='AAPL', price=176.0, quant=2)
    # print(result)

    # Place order - sell
    result = wb.place_sell_order(stock='AAPL', price=175.82, quant=1)
    print(result)


"""
endpoints.py
    def stock_id(self, stock, region_code):
        return f'{self.base_options_gw_url}/search/pc/tickers?keyword={stock}&pageIndex=1&pageSize=20'
"""