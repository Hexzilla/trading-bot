from pandas import Series, DataFrame


class BaseIndicator:
    def __int__(self, length: int):
        self.length = length

    def execute(self, df: DataFrame):
        pass
