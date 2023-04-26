import datetime
from pprint import pprint

import pytz
from pandas import DataFrame
from tda.client.base import BaseClient

from brokers.tda.auth.custom_auth import *
from core.broker_client import BrokerClient


class BrokerClient(BrokerClient):
    tda_client = None

    def __init__(self, api_key):
        super().__init__(api_key)
        self.get_client()

    def get_client(self):

        if self.tda_client is not None:
            return self.tda_client

        token_path = get_token_path(self.api_key)
        if os.path.isfile(token_path):
            # Decrypt the API_KEY_HERE
            client = client_from_token_file(token_path, self.api_key, asyncio=False, enforce_enums=True)
            get_logger().info('Returning client loaded from token file \'%s\'', token_path)

            self.tda_client = client
            return self.tda_client

    def get_quotes(self, tickers) -> DataFrame:
        response = self.tda_client.get_quotes(tickers)
        assert response.status_code == 200, response.raise_for_status()
        return DataFrame.from_dict(response.json(), orient='index')

    def get_option_chains(self, tickers) -> DataFrame:
        for ticker in tickers:
            response = self.tda_client.get_option_chains(ticker, strike_count=2, days_to_expiration=1,
                                                         to_date=datetime.datetime.now(pytz.timezone('US/Eastern')) +
                                                                 datetime.timedelta(days=2))
            assert response.status_code == 200, response.raise_for_status()
            pprint(response.json())
            yield DataFrame.from_dict(response.json())

    def get_bars(self, tickers, period_type=BaseClient.PriceHistory.PeriodType.DAY,
                 period=BaseClient.PriceHistory.Period.THREE_DAYS,
                 frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                 frequency=BaseClient.PriceHistory.Frequency.EVERY_MINUTE, ext_hours_data=False):
        for ticker in tickers:
            response = self.tda_client.get_price_history(ticker, period_type=period_type, period=period,
                                                         frequency_type=frequency_type, frequency=frequency,
                                                         need_extended_hours_data=ext_hours_data)
            assert response.status_code == 200, response.raise_for_status()
            yield DataFrame.from_dict(response.json())
