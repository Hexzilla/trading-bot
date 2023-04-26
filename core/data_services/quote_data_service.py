from core.broker_client import BrokerClient
from core.data_services.http_data_service import HttpDataService


class QuoteDataService(HttpDataService):
    def __init__(self, proxy_broker_client: BrokerClient, tickers: list[str]):
        self.proxy_broker_client = proxy_broker_client
        self.tickers = tickers

        assert tickers is not None or len(tickers) > 0, 'Invalid ticker list'

    def _acquire_data(self):
        return self.proxy_broker_client.get_quotes(self.tickers)
