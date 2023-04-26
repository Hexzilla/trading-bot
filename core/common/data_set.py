from pandas import DataFrame


class DataSet:
    def __init__(self,
                 latest_bars: DataFrame = None,
                 latest_quotes: DataFrame = None,
                 latest_option_chains: DataFrame = None):
        self.bars = latest_bars
        self.quotes = latest_quotes
        self.option_chains = latest_option_chains

    def has_data(self):
        return self.bars is not None or self.quotes is not None or self.option_chains is not None

    def __str__(self):
        return 'Bars: ' + str(self.bars) + '\nQuotes: ' + str(self.quotes) + '\nOption Chains: ' + str(self.option_chains)
