from webull import paper_webull

did = "72b0c5e07699488580fb5a30b9a4ecdc"


class paper_webull_wrapper(paper_webull):
    def set_did(self, did):
        self._set_did(did)

    def set_region_code(self, region_code):
        self._region_code = region_code

    def get_account_id(self):
        return self._account_id


def webull_login(email, password):
    wb = paper_webull_wrapper()
    wb.set_did(did)
    wb.set_region_code(1)

    wb.login(email, password, 'Windows Chrome')

    account = wb.get_account()
    print(account)
