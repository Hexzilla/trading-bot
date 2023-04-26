from abc import abstractmethod

from pandas import DataFrame
from tda.client import Client

from core.common.subject import Subject


class BrokerClient(Subject):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_client(self) -> object:
        pass

    @abstractmethod
    def get_quotes(self, tickers) -> DataFrame:
        pass

    @abstractmethod
    def get_option_chains(self, tickers) -> DataFrame:
        pass

    @abstractmethod
    def get_bars(self, tickers, period_type=Client.PriceHistory.PeriodType.DAY,
                 period=Client.PriceHistory.Period.THREE_DAYS,
                 frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                 frequency=Client.PriceHistory.Frequency.EVERY_MINUTE, ext_hours_data=False) -> DataFrame:
        pass


