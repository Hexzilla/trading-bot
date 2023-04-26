from tda.client.base import BaseClient

from core.broker_client import BrokerClient
from core.data_services.http_data_service import HttpDataService


class BarDataService(HttpDataService):
    def __init__(self, proxy_broker_client: BrokerClient, tickers: list[str],
                 period_type=BaseClient.PriceHistory.PeriodType.DAY,
                 period=BaseClient.PriceHistory.Period.THREE_DAYS,
                 frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                 frequency=1, ext_hours_data=False):
        self.proxy_broker_client = proxy_broker_client
        self.tickers = tickers
        self.period_type = period_type
        self.period = period
        self.frequency_type = frequency_type
        self.frequency = frequency
        self.ext_hours_data = ext_hours_data

        assert tickers is not None or len(tickers) > 0, 'Invalid ticker list'

    def _acquire_data(self):
        return self.proxy_broker_client.get_bars(self.tickers,
                                                 self.period_type,
                                                 self.period,
                                                 self.frequency_type,
                                                 self.frequency,
                                                 self.ext_hours_data)
