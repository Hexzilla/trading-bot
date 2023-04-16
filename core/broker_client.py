from pandas import DataFrame
from tda.client import Client


class BaseBrokerClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def _get_client(self) -> object:
        pass

    def get_quotes(self, tickers) -> DataFrame:
        pass

    def get_bars(self, tickers, period_type=Client.PriceHistory.PeriodType.DAY,
                 period=Client.PriceHistory.Period.THREE_DAYS,
                 frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                 frequency=Client.PriceHistory.Frequency.EVERY_MINUTE) -> DataFrame:
        pass
