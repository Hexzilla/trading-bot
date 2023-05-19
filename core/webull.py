from webull import paper_webull
from brokers.tda.db.db_account import insert_account

email = 'thegreatone150@gmail.com'
password = 'Tank2013!'
deviceId = "72b0c5e07699488580fb5a30b9a4ecdc"


class paper_webull_wrapper(paper_webull):
    def set_did(self, did):
        self._set_did(did)

    def set_region_code(self, region_code):
        self._region_code = region_code

    def get_account_id(self):
        return self._account_id

    def login_with_email(self, _email, _password):
        result = self.login(_email, _password, 'Windows Chrome')
        return 'accessToken' in result


def webull_login():
    wb = paper_webull_wrapper()
    wb.set_did(deviceId)
    wb.set_region_code(1)

    result = wb.login_with_email(email, password)
    if result:
        account_id = wb.get_account_id()
        insert_account({account_id, True})
