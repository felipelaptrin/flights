import re
import time
from datetime import datetime
from typing import List, Tuple

from config import DATE_FORMAT, GOOGLE_FLIGHTS_URL
from crawler import Crawler
from models import Flights
from selenium.webdriver.common.keys import Keys


class GoogleFlightsCrawler(Crawler):
    def __init__(self, flight: Flights):
        super().__init__(flight)
        self.url = f"{GOOGLE_FLIGHTS_URL}&curr={self.currency}"

    def __input_date(
        self, date: datetime, xpath: str, xpath_selected: str, reset_dates: bool = False
    ) -> None:
        RESET_BUTTON_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/button/span"

        date = date.strftime("%a, %b %-d")
        self.wait_clickable(5, xpath)
        self.click(xpath)
        if reset_dates:
            self.wait_clickable(5, RESET_BUTTON_XPATH)
            time.sleep(
                0.8
            )  #! Find way to remove this sleep! Wait_clickable in the RESET_BUTTON is not working
            self.click(RESET_BUTTON_XPATH)
        self.wait_clickable(5, xpath_selected)
        self.send(xpath_selected, [Keys.BACK_SPACE, date, Keys.ENTER])
        self.assert_inputed_value(xpath_selected, date)

    def set_dates(self) -> None:
        XPATH_DEPARTURE_DATE_ORIGIN = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input"
        XPATH_DEPARTURE_DATE_ORIGIN_SELECTED = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input"

        XPATH_DEPARTURE_DATE_DESTINATION_SELECTED = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input"

        DONE_BUTTON_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button/span"

        SEARCH_BUTTON_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/span[2]"

        self.logger.info("Setting dates...")
        self.logger.info("Setting origin date")
        self.__input_date(
            self.departure_date_origin,
            XPATH_DEPARTURE_DATE_ORIGIN,
            XPATH_DEPARTURE_DATE_ORIGIN_SELECTED,
            True,
        )
        self.logger.info("Setting destination date")
        self.__input_date(
            self.departure_date_destination,
            XPATH_DEPARTURE_DATE_DESTINATION_SELECTED,
            XPATH_DEPARTURE_DATE_DESTINATION_SELECTED,
        )
        self.click(DONE_BUTTON_XPATH)
        self.wait_clickable(1, SEARCH_BUTTON_XPATH)
        self.click(SEARCH_BUTTON_XPATH)
        self.logger.info("Dates set!")

    def __input_itinerary(self, place: str, xpath: str, xpath_selected: str) -> None:
        self.logger.info("Finding input box to set itinerary...")
        self.clear(xpath)
        self.send(xpath, place[0])
        self.wait_clickable(5, xpath_selected)
        self.send(xpath_selected, [place[1:], Keys.ENTER])
        self.assert_inputed_value(xpath, place)

    def set_itineraty(self) -> None:
        self.logger.info("Setting itinerary...")
        XPATH_ORIGIN = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input"
        XPATH_ORIGIN_SELECTED = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input"
        XPATH_DESTINATION = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input"
        XPATH_DESTINATION_SELECT = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input"

        self.__input_itinerary(self.origin, XPATH_ORIGIN, XPATH_ORIGIN_SELECTED)
        self.__input_itinerary(self.destination, XPATH_DESTINATION, XPATH_DESTINATION_SELECT)
        self.logger.info("Itinerary set correctly!")

    def wait_generic_destination_search_results(self, max_timeout: int = 15) -> None:
        self.logger.info("Waiting results to show up...")
        path = self.__get_full_xpath_travel_destination_info(1)

        try:
            self.wait_presence(max_timeout, path)
            self.logger.info("Results loaded...")
        except:
            print("Not able to load results!")

    def wait_specific_destination_search_results(self, max_timeout: int = 15) -> None:
        self.logger.info("Waiting results to show up...")
        XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li[1]/div/div[3]/div/div/button/div[3]"

        try:
            self.wait_clickable(max_timeout, XPATH)
            self.logger.info("Results loaded...")
        except:
            print("Not able to load results!")

    def __get_full_xpath_travel_destination_info(self, result_index: int) -> str:
        FULL_XPATH = f"/html/body/c-wiz[3]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/main/div/div[2]/div/ol/li[{result_index}]/div/div[2]"

        return FULL_XPATH

    def get_destination_info(self, result_index: int) -> str:
        path = self.__get_full_xpath_travel_destination_info(result_index)
        info_not_parsed = self.select(path).text

        return info_not_parsed

    def __get_price_and_currency(self, price: str) -> Tuple[str, int]:
        number = []
        currency = []
        for char in price:
            if char.isdigit():
                number.append(char)
            else:
                currency.append(char) if char not in [",", ".", " "] else None

        currency = "".join(currency)
        number = int("".join(number))

        return (number, currency)

    def parse_destination_info_generic_destination(self, info_not_parsed: str) -> dict:
        info_not_parsed = info_not_parsed.split("\n")

        if len(info_not_parsed) == 4:
            destination, stops, duration, price = info_not_parsed
        elif len(info_not_parsed) == 5:
            destination, price, stops, duration, _ = info_not_parsed
        else:
            raise Exception(f"Results couldn't be parsed: {info_not_parsed}")
        destination = destination.strip()

        number_of_stops = int(stops.split("stop")[0])

        duration_hours = int(duration.split("hr")[0])
        if "min" in duration:
            duration_min = re.search("%s(.*)%s" % ("hr", "min"), duration).group(1)
            duration_min = int(duration_min.strip())
        else:
            duration_min = 0
        duration_hours_float = float(duration_hours + duration_min / 60)

        price, currency = self.__get_price_and_currency(price)
        price = int(price)

        return {
            "destination": destination,
            "duration": duration_hours_float,
            "stops": number_of_stops,
            "price": price,
            "currency": currency,
        }

    def __get_all_flight_results_generic_destination(self) -> List[dict]:
        self.logger.info("Retrieving all flights results...")
        MAX_NUMBER_OF_RESULTS = 40

        results = []
        for i in range(MAX_NUMBER_OF_RESULTS):
            try:
                info = self.get_destination_info(i)
                parsed_info = self.parse_destination_info_generic_destination(info)
                parsed_info["id"] = self.timestamp
                parsed_info["stay_days"] = self.stay_days
                parsed_info["departure_date_origin"] = self.departure_date_origin.strftime(
                    DATE_FORMAT
                )
                parsed_info[
                    "departure_date_destination"
                ] = self.departure_date_destination.strftime(DATE_FORMAT)
                results.append(parsed_info)
            except Exception as e:
                self.logger.error(f"Could not parse flight result => {e}")

        self.logger.info("Flights results retrieved successfully")
        return results

    def parse_destination_info_specific_destination(self, info_not_parsed: str) -> dict:
        info_not_parsed = info_not_parsed.split("\n")
        self.logger.info(f"To be parsed => {info_not_parsed}")

        if len(info_not_parsed) == 12:
            (
                _,
                _,
                _,
                _,
                duration,
                airports,
                number_of_stops,
                _,
                _,
                _,
                price,
                _,
            ) = info_not_parsed
        elif len(info_not_parsed) == 13:
            (
                _,
                _,
                _,
                _,
                _,
                duration,
                airports,
                number_of_stops,
                _,
                _,
                _,
                price,
                _,
            ) = info_not_parsed
        else:
            raise Exception(f"Results couldn't be parsed: {info_not_parsed}")

        number_of_stops = int(number_of_stops.split(" ")[0])

        duration_hours = int(duration.split("h")[0].strip())
        if "min" in duration:
            hour = "hr" if "hr" in duration else "h"
            duration_min = re.search("%s(.*)%s" % (hour, "min"), duration).group(1)
            print(duration_min)
            duration_min = int(duration_min.strip())
        else:
            duration_min = 0
        duration_hours_float = float(duration_hours + duration_min / 60)

        price, currency = self.__get_price_and_currency(price)

        destination = airports.split("–")[-1]

        return {
            "destination": destination,
            "duration": duration_hours_float,
            "stops": number_of_stops,
            "price": price,
            "currency": currency,
        }

    def crawl_generic_destinations(
        self,
    ) -> List[dict]:
        self.driver.get(self.url)
        self.set_itineraty()
        self.set_dates()
        self.wait_generic_destination_search_results()
        results = self.__get_all_flight_results_generic_destination()

        self.logger.info(f"Crawled results => {results}")

        return results

    def __get_all_flight_results_specific_destination(self) -> List[dict]:
        self.logger.info("Retrieving all flights results...")
        MAX_NUMBER_OF_RESULTS = 40
        BEST_FLIGHTS_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li[REPLACE]"
        OTHER_FLIGHTS_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[5]/ul/li[REPLACE]"
        results = []
        for i in range(MAX_NUMBER_OF_RESULTS):
            try:
                for xpath in [OTHER_FLIGHTS_XPATH, BEST_FLIGHTS_XPATH]:
                    flight_xpath = xpath.replace("REPLACE", str(i))
                    flight_info = self.select(flight_xpath).text
                    flight_info_parsed = self.parse_destination_info_specific_destination(
                        flight_info
                    )

                    flight_info_parsed["id"] = self.timestamp
                    flight_info_parsed["stay_days"] = self.stay_days
                    flight_info_parsed[
                        "departure_date_origin"
                    ] = self.departure_date_origin.strftime(DATE_FORMAT)
                    flight_info_parsed[
                        "departure_date_destination"
                    ] = self.departure_date_destination.strftime(DATE_FORMAT)
                    results.append(flight_info_parsed)
            except Exception as e:
                self.logger.error(f"Could not parse flight result => {e}")

        self.logger.info("Flights results retrieved successfully")
        return results

    def crawl_specific_destination(self):
        self.driver.get(self.url)
        self.set_itineraty()
        self.set_dates()
        self.wait_specific_destination_search_results()
        results = self.__get_all_flight_results_specific_destination()
        self.logger.info(f"Crawled results => {results}")

        return results
