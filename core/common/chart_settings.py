from tda.client.base import BaseClient


class ChartSettings:
    def __init__(self, period_type=BaseClient.PriceHistory.PeriodType.DAY,
                 period=BaseClient.PriceHistory.Period.THREE_DAYS,
                 frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                 frequency=1, ext_hours_data=False):
        self.period_type = BaseClient.PriceHistory.PeriodType.DAY,
        self.period = BaseClient.PriceHistory.Period.THREE_DAYS,
        self.frequency_type = BaseClient.PriceHistory.FrequencyType.MINUTE,
        self.frequency = 1
        self.ext_hours_data = ext_hours_data
