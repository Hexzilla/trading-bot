import atexit
import platform as p
from sys import platform

from from_root import from_root
from selenium.webdriver.chrome.service import Service


def make_webdriver():
    # Import selenium here because it's slow to import
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if platform == "linux" or platform == "linux2":
        options.add_argument('--headless')
        service = Service(str(from_root()) + '/auth/drivers/linux/chromedriver')
        options.binary_location = '/usr/bin/brave-browser'
    elif platform == "darwin":
        is_arm_processor = p.processor() == 'arm'

        if is_arm_processor:
            service = Service(str(from_root()) + '/auth/drivers/macos/arm/chromedriver')
        else:
            service = Service(str(from_root()) + '/auth/drivers/macos/x64/chromedriver')
        options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    elif platform == "win32":
        service = Service(str(from_root()) + '/auth/drivers/windows/chromedriver')
        options.binary_location = 'C:\\ProgramFiles\\Google\\Chrome\\Application\\chrome.exe'

    driver = webdriver.Chrome(service=service, options=options,
                              service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    atexit.register(lambda: driver.quit())

    return driver
