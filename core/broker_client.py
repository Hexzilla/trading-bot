from abc import abstractmethod
from typing import final

from pandas import DataFrame
from tda.client import Client

from core.data_set import DataSet


class BaseBrokerClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def _get_client(self) -> object:
        pass

    @abstractmethod
    def get_quotes(self, tickers) -> DataFrame:
        pass

    @abstractmethod
    def get_bars(self, tickers, period_type=Client.PriceHistory.PeriodType.DAY,
                 period=Client.PriceHistory.Period.THREE_DAYS,
                 frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                 frequency=Client.PriceHistory.Frequency.EVERY_MINUTE, ext_hours_data=False) -> DataFrame:
        pass

    @final
    def get_data(self, tickers, period_type=Client.PriceHistory.PeriodType.DAY,
                 period=Client.PriceHistory.Period.THREE_DAYS,
                 frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                 frequency=Client.PriceHistory.Frequency.EVERY_MINUTE, ext_hours_data=False) -> DataFrame:
        quotes_df = self.get_quotes(tickers)
        bars_df = self.get_bars(tickers, period_type, period, frequency_type, frequency, ext_hours_data)

        for bars in bars_df:
            symbol = bars['symbol'][0]
            yield DataSet(symbol, bars, quotes_df.loc[symbol])


