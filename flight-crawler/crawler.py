import logging
from datetime import datetime
from logging import Logger
from tempfile import mkdtemp
from typing import Any, List, Union

import undetected_chromedriver as uc
from config import LOGGER_LEVEL, RUN_LOCALLY_WITH_HEADER
from models import Flights
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Crawler:
    CHROME_BINARY_PATH = "/opt/chrome/chrome"
    CHROME_WEBDRIVER_BINARY_PATH = "/opt/chromedriver"

    def __init__(self, flight: Flights):
        self.__logger_level = LOGGER_LEVEL
        self.logger = self.__get_logger()
        self.driver = self.__get_driver()
        self.timestamp = datetime.strftime(datetime.now(), "%d%m%Y%H%M%S%f")
        self.origin = flight.origin
        self.destination = flight.destination
        self.departure_date_origin = flight.departure_date_origin
        self.departure_date_destination = flight.departure_date_destination
        self.stay_days = (self.departure_date_destination - self.departure_date_origin).days

    def __get_driver(self) -> webdriver.Chrome:
        self.logger.debug("Setting Selenium Driver to use Google Chrome...")
        if RUN_LOCALLY_WITH_HEADER:
            driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()))
            self.logger.debug("Selenium Driver set correctly to work locally with headers")
            return driver
        options = uc.ChromeOptions()
        # options.binary_location = self.CHROME_BINARY_PATH
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")

        driver = uc.Chrome(options=options)
        self.logger.debug("Selenium Driver set correctly")
        return driver

    def __get_logger(self) -> Logger:
        logger = logging.getLogger()
        logger.setLevel(self.__logger_level)
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s: %(message)s", level=self.__logger_level
        )

        return logger

    def wait_presence(self, max_timeout: int, xpath: str):
        WebDriverWait(self.driver, max_timeout).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )

    def wait_clickable(self, max_timeout: int, xpath: str):
        WebDriverWait(self.driver, max_timeout).until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )

    def select(self, xpath: str) -> WebElement:
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def click(self, xpath: str) -> None:
        self.select(xpath).click()

    def send(self, xpath: str, text: Union[List[Any], Any]):
        self.select(xpath).send_keys(text)

    def clear(self, xpath: str) -> None:
        self.select(xpath).clear()

    def get_input_box_value(self, xpath: str) -> str:
        value = self.select(xpath).get_attribute("value")
        return value

    def assert_inputed_value(self, xpath: str, expected_value: str, strict: bool = False):
        actual_box_value = self.get_input_box_value(xpath)
        if not strict:
            actual_box_value = actual_box_value.lower()
            expected_value = expected_value.lower()
        if actual_box_value != expected_value:
            error_message = f"Inputted date is wrong! You wanted to input '{expected_value}' but '{actual_box_value}' was the input"
            self.logger.error(error_message)
            raise Exception(error_message)
