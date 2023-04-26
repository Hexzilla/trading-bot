import time

from tda.client.base import BaseClient

from core.common.chart_settings import ChartSettings
from core.common.start_mode import StartMode

seconds_per_day = 24 * 60 * 60
data_polling_interval_in_milliseconds = 500
start_mode = StartMode.PULLING
default_chart_settings: ChartSettings = ChartSettings(period_type=BaseClient.PriceHistory.PeriodType.DAY,
                                                      period=BaseClient.PriceHistory.Period.THREE_DAYS,
                                                      frequency_type=BaseClient.PriceHistory.FrequencyType.MINUTE,
                                                      frequency=1, ext_hours_data=False)

end_time_in_seconds = time.time()
start_time_in_seconds = end_time_in_seconds - seconds_per_day * 90
