import asyncio
import time

from stopwatch import Stopwatch


class HttpDataService:
    _last_update_time = None
    _latest_data = None

    async def run(self, polling_interval_in_milliseconds):
        stopwatch = Stopwatch()
        while True:
            stopwatch.reset()
            stopwatch.start()

            # Get latest data
            self._latest_data = self._acquire_data()

            # stop and calculate the wait time
            stopwatch.stop()
            wait_time_in_seconds = (polling_interval_in_milliseconds - stopwatch.duration) / 1000.0

            self._last_update_time = time.time()

            # Sleep
            await asyncio.sleep(wait_time_in_seconds)

    async def _acquire_data(self):
        pass

    @property
    def last_update_time(self):
        return self._last_update_time

    @property
    def latest_data(self):
        return self._latest_data
