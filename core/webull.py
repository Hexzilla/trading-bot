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

    def get_account_id(self):
        return self._account_id

    def login_with_email(self, email, password):
        result = self.login(email, password, 'Windows Chrome')
        return 'accessToken' in result


def webull_login():
    wb = paper_webull_wrapper()
    wb.set_did(_deviceId)
    wb.set_region_code(_regionId)

    result = wb.login_with_email(_email, _password)
    if result:
        account_id = wb.get_account_id()
        insert_account({account_id, True})
