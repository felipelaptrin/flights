import logging
import os
import re
import time
from datetime import datetime
from logging import Logger
from tempfile import mkdtemp
from typing import List

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class GoogleFlightsCrawler:
    CHROME_BINARY_PATH = "/opt/chrome/chrome"
    CHROME_WEBDRIVER_BINARY_PATH = "/opt/chromedriver"

    def __init__(
        self,
        origin: str,
        destination: str,
        departure_date_origin: str,
        departure_date_destination: str,
    ):
        self.__logger_level = os.getenv("LOGGER_LEVEL", "INFO")
        self.logger = self.__get_logger()
        self.driver = self.__get_driver()
        self.timestamp = datetime.strftime(datetime.now(), "%d%m%Y%H%M%S%f")
        self.origin = origin
        self.destination = destination
        self.departure_date_origin = datetime.strptime(departure_date_origin, "%d/%m/%Y")
        self.departure_date_destination = datetime.strptime(
            departure_date_destination, "%d/%m/%Y"
        )
        self.stay_days = (self.departure_date_destination - self.departure_date_origin).days

    def __get_logger(self) -> Logger:
        logger = logging.getLogger()
        logger.setLevel(self.__logger_level)
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s: %(message)s", level=self.__logger_level
        )

        return logger

    def __get_driver(self) -> webdriver.Chrome:
        self.logger.debug("Setting Selenium Driver to use Google Chrome...")
        if os.getenv("RUN_LOCALLY_WITH_HEADER", "FALSE").upper() == "TRUE":
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
            )
            self.logger.debug("Selenium Driver set correctly to work locally with headers")
            return driver
        options = webdriver.ChromeOptions()
        options.binary_location = self.CHROME_BINARY_PATH
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

        driver = webdriver.Chrome(self.CHROME_WEBDRIVER_BINARY_PATH, options=options)
        self.logger.debug("Selenium Driver set correctly")
        return driver

    def __input_date(self, date: datetime, xpath: str, xpath_continue: str) -> None:
        CHARS_TO_DELETE_IN_DATE_INPUT_FIELD = 30

        date = date.strftime("%a, %b %-d")
        date_element = self.driver.find_element(By.XPATH, xpath)
        date_element.click()
        time.sleep(0.5)
        date_element = self.driver.find_element(By.XPATH, xpath_continue)
        date_element.send_keys(Keys.END)
        for i in range(CHARS_TO_DELETE_IN_DATE_INPUT_FIELD):
            date_element.send_keys(Keys.BACKSPACE)
        date_element.clear()
        date_element.send_keys(date)
        time.sleep(0.5)
        date_element.send_keys(Keys.ENTER)

    def set_dates(self) -> None:
        XPATH_DEPARTURE_DATE_ORIGIN = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/div/input"
        XPATH_DEPARTURE_DATE_ORIGIN_CONTINUE = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/div[1]/div/div[1]/div/input"

        # For departure date destination the values are equal because the box to select the date is already opened
        XPATH_DEPARTURE_DATE_DESTINATION = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/div[1]/div/div[2]/div/input"
        XPATH_DEPARTURE_DATE_CONTINUE_DESTINATION = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/div[1]/div/div[2]/div/input"

        XPATH_DONE_BUTTON = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/div[1]/button"

        XPATH_FLEXIBLE_DATES = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div"
        XPATH_SPECIFIC_DATES = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/span/button[1]"

        self.logger.info("Setting dates...")
        try:
            self.__input_date(
                self.departure_date_origin,
                XPATH_DEPARTURE_DATE_ORIGIN,
                XPATH_DEPARTURE_DATE_ORIGIN_CONTINUE,
            )
            time.sleep(1.0)
        except:
            self.driver.find_element(By.XPATH, XPATH_FLEXIBLE_DATES).click()
            time.sleep(0.2)
            self.driver.find_element(By.XPATH, XPATH_SPECIFIC_DATES).click()
            self.__input_date(
                self.departure_date_origin,
                XPATH_DEPARTURE_DATE_ORIGIN_CONTINUE,
                XPATH_DEPARTURE_DATE_ORIGIN_CONTINUE,
            )
            time.sleep(1.0)
        self.__input_date(
            self.departure_date_destination,
            XPATH_DEPARTURE_DATE_DESTINATION,
            XPATH_DEPARTURE_DATE_CONTINUE_DESTINATION,
        )
        done_button = self.driver.find_element(By.XPATH, XPATH_DONE_BUTTON)
        done_button.click()
        self.logger.info("Dates set!")

    def __input_itinerary(self, place: str, xpath: str, xpath_continue: str) -> None:
        self.logger.debug("Finding input box to set itinerary...")
        origin = self.driver.find_element(By.XPATH, xpath)
        origin.clear()
        origin.send_keys(place[0])
        origin = self.driver.find_element(By.XPATH, xpath_continue)
        origin.send_keys(place[1:])
        time.sleep(0.5)
        origin.send_keys(Keys.ENTER)
        time.sleep(0.5)

    def set_itineraty(self, origin: str, destination: str) -> None:
        self.logger.info("Setting itinerary...")
        XPATH_ORIGIN = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/input"
        XPATH_ORIGIN_CONTINUE = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/input"

        XPATH_DESTINATION = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/input"
        XPATH_DESTINATION_CONTINUE = "/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/input"

        self.__input_itinerary(origin, XPATH_ORIGIN, XPATH_ORIGIN_CONTINUE)
        self.__input_itinerary(destination, XPATH_DESTINATION, XPATH_DESTINATION_CONTINUE)
        self.logger.info("Itinerary set correctly!")

    def wait_results(self, max_timeout: int = 15) -> None:
        self.logger.info("Waiting results to show up...")

        path = self.__get_full_xpath_travel_destination_info(1)

        try:
            WebDriverWait(self.driver, max_timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, path))
            )
            print("Results loaded...")
        except:
            print("Not able to load results!")

    def __get_full_xpath_travel_destination_info(self, result_index: int) -> str:
        FULL_XPATH = f"/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/main/div/div[2]/div/ol/li[{result_index}]/div/div[2]"

        return FULL_XPATH

    def get_destination_info(self, result_index: int) -> str:
        path = self.__get_full_xpath_travel_destination_info(result_index)
        info_not_parsed = self.driver.find_element(By.XPATH, path).text

        return info_not_parsed

    def parse_destination_info(self, info_not_parsed: str) -> dict:
        info_not_parsed = info_not_parsed.split("\n")

        if len(info_not_parsed) == 4:
            destination, stops, duration, price = info_not_parsed
        elif len(info_not_parsed) == 5:
            destination, price, stops, duration, _ = info_not_parsed
        else:
            raise Exception("Results couldn't be parsed")
        destination = destination.strip()

        number_of_stops = int(stops.split("stop")[0])

        duration_hours = int(duration.split("hr")[0])
        if "min" in duration:
            duration_min = re.search("%s(.*)%s" % ("hr", "min"), duration).group(1)
            duration_min = int(duration_min.strip())
        else:
            duration_min = 0
        duration_hours_float = float(duration_hours + duration_min / 60)

        price = price.replace("R$", "").replace(",", "")
        price = int(price)

        return {
            "destination": destination,
            "duration": duration_hours_float,
            "stops": number_of_stops,
            "price": price,
        }

    def __get_all_flight_results(self) -> List[dict]:
        self.logger.info("Retrieving all flights results...")
        MAX_NUMBER_OF_RESULTS = 40

        results = []
        for i in range(MAX_NUMBER_OF_RESULTS):
            try:
                info = self.get_destination_info(i)
                parsed_info = self.parse_destination_info(info)
                parsed_info["id"] = self.timestamp
                parsed_info["stay_days"] = self.stay_days
                parsed_info["departure_date_origin"] = self.departure_date_origin.strftime(
                    "%d/%m/%Y"
                )
                parsed_info[
                    "departure_date_destination"
                ] = self.departure_date_destination.strftime("%d/%m/%Y")
                results.append(parsed_info)
            except Exception as e:
                self.logger.error(f"Could not parse flight result because: {str(e)}")

        self.logger.info("Flights results retrieved successfully")
        return results

    def crawl_generic_destinations(
        self,
    ) -> List[dict]:
        self.driver.get(os.getenv("URL"))
        self.set_itineraty(self.origin, self.destination)
        self.set_dates()
        self.wait_results()
        results = self.__get_all_flight_results()

        return results


class Database:
    def __init__(self):
        self.__logger_level = os.getenv("LOGGER_LEVEL", "INFO")
        self.logger = self.__get_logger()
        self.collection = self.__connect_db()

    def __get_logger(self) -> Logger:
        logger = logging.getLogger()
        logger.setLevel(self.__logger_level)
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s: %(message)s", level=self.__logger_level
        )

        return logger

    def __connect_db(self):
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        cluster_name = os.getenv("DB_CLUSTER")
        cluster_id = os.getenv("CLUSTER_ID")
        collection_name = os.getenv("DB_COLLECTION")
        try:
            db_connection_string = f"mongodb+srv://{user}:{password}@{cluster_name}.{cluster_id}.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(db_connection_string)
            print(client)
            db = client[db_name]
            print(db)
            collection = db[collection_name]
            print(collection)
        except Exception as e:
            self.logger.error("Could not stablish a connection with the database")
            raise Exception(f"Could not connect to DB due to the following error: {e}")

        return collection

    def store_results(
        self,
        documents: List[dict],
    ) -> None:
        self.collection.insert_many(documents)


def handler(event=None, context=None):
    print("STARTED!")
    try:
        departure_date_origin = event["departureDateOrigin"]
        departure_date_destination = event["departureDateDestination"]
        origin = event["origin"]
        destination = event["destination"]

        crawler = GoogleFlightsCrawler(
            origin, destination, departure_date_origin, departure_date_destination
        )
        results = crawler.crawl_generic_destinations()
        print(results)

        Database().store_results(results)

        return {"statusCode": 200, "body": "Crawler run successfully"}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": f"Something went wrong: {str(e)}"}
