import json
import os
import pickle
from webull import paper_webull
from brokers.tda.db.db_account import insert_account

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


    def login_with_email(self, email, password):
        result = self.login(email, password, 'Windows Chrome', save_token=True)
        return 'accessToken' in result


def create_webull():
    wb = paper_webull_wrapper()
    wb.set_did(_deviceId)
    wb.set_region_code(_regionId)

    result = wb.login_with_credentials()
    if not result:
        result = wb.login_with_email(_email, _password)

    if result:
        account_id = wb.account_id()
        insert_account((account_id, True))
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
    orders = wb.get_current_orders()
    print(orders)

    # Place order
    result = wb.place_order(stock='AAPL', price=90.0, qty=2)
    print(result)
