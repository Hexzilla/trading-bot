from pprint import pprint
from time import sleep
from tda import client
from auth.custom_auth import *

API_KEY = '<API_KEY_HERE>'


def get_logger():
    return logging.getLogger(__name__)


def get_client():
    token_path = get_token_path(API_KEY)
    if os.path.isfile(token_path):
        c = client_from_token_file(token_path, API_KEY, asyncio=False, enforce_enums=True)
        get_logger().info('Returning client loaded from token file \'%s\'', token_path)

        return c


def get_quotes(tickers):
    c = get_client()

    for ticker in tickers:
        q = c.get_quotes(ticker)
        yield json.dumps(q.json(), indent=4)

        sleep(2)
        r = c.get_price_history(ticker,
                                period_type=client.Client.PriceHistory.PeriodType.DAY,
                                period=client.Client.PriceHistory.Period.TEN_DAYS,
                                frequency_type=client.Client.PriceHistory.FrequencyType.MINUTE,
                                frequency=client.Client.PriceHistory.Frequency.EVERY_MINUTE)
        # assert r.status_code == 200, r.raise_for_status()
        # print(json.dumps(r.json(), indent=4))


# Press the green button in the gutter to run the script.
tickers = ['AAPL', 'SPY', 'SPX', 'INTC', 'TSLA']

if __name__ == '__main__':
    for quote in get_quotes(tickers):
        pprint(quote)
