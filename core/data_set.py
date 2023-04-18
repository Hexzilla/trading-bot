from pandas import DataFrame


class DataSet:
    def __init__(self, symbol: str, latest_bars: DataFrame, latest_quote: DataFrame):
        self.symbol = symbol
        self.quote = latest_quote
        self.bars = latest_bars
