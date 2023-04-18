from pandas import DataFrame
from tda.client.base import BaseClient

from brokers.tda.auth.custom_auth import *
from core.broker_client import BaseBrokerClient


class BrokerClient(BaseBrokerClient):
    def __init__(self, api_key):
        BaseBrokerClient.__init__(self, api_key)

    def _get_client(self):
        token_path = get_token_path(self.api_key)
        if os.path.isfile(token_path):
            # Decrypt the API_KEY_HERE
            client = client_from_token_file(token_path, self.api_key, asyncio=False, enforce_enums=True)
            get_logger().info('Returning client loaded from token file \'%s\'', token_path)

            return client

    def get_quotes(self, tickers) -> DataFrame:
        tda_client: Client = self._get_client()

        response = tda_client.get_quotes(tickers)
        assert response.status_code == 200, response.raise_for_status()
        return DataFrame.from_dict(response.json(), orient='index')

    def get_bars(self, tickers, period_type=BaseClient.PriceHistory.PeriodType.DAY,
                 period=BaseClient.PriceHistory.Period.THREE_DAYS,
                 frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                 frequency=BaseClient.PriceHistory.Frequency.EVERY_MINUTE, ext_hours_data=False):
        tda_client: Client = self._get_client()

        for ticker in tickers:
            response = tda_client.get_price_history(ticker, period_type=period_type, period=period,
                                                    frequency_type=frequency_type, frequency=frequency,
                                                    need_extended_hours_data=ext_hours_data)
            assert response.status_code == 200, response.raise_for_status()
            yield DataFrame.from_dict(response.json())
