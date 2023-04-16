from pandas import DataFrame


class Quote:
    def __init__(self, data: DataFrame):
        self.data = data
