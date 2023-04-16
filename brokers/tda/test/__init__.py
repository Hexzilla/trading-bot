import os

from tda.client.base import BaseClient

from brokers.tda.broker_client import BrokerClient


def test(api_key, tickers):
    tda_client = BrokerClient(api_key)

    for quote in tda_client.get_quotes(tickers):
        print(str(quote.data))

    for bar in tda_client.get_bars(tickers,
                                       period_type=BaseClient.PriceHistory.PeriodType.DAY,
                                       period=BaseClient.PriceHistory.Period.THREE_DAYS,
                                       frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                                       frequency=BaseClient.PriceHistory.Frequency.EVERY_MINUTE):
        print(str(bar.data))


if __name__ == '__main__':
    stock_tickers = ['SPY', 'AAPL', 'TSLA']
    td_api_key = os.getenv('TDA_API_KEY')

    test(td_api_key, stock_tickers)