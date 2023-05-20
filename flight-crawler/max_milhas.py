import time
from datetime import datetime

from config import MAX_MILHAS_URL
from crawler import Crawler
from models import Flights


class MaxMilhasCrawler(Crawler):
    def __init__(self, flight: Flights):
        super().__init__(flight)
        self.url = MAX_MILHAS_URL

    def datetime_to_str_ptbr(self, date: datetime):
        month = date.month
        if month == 1:
            month_name = "janeiro"
        elif month == 2:
            month_name = "fevereiro"
        elif month == 3:
            month_name = "março"
        elif month == 4:
            month_name = "abril"
        elif month == 5:
            month_name = "maio"
        elif month == 6:
            month_name = "junho"
        elif month == 7:
            month_name = "julho"
        elif month == 8:
            month_name = "agosto"
        elif month == 9:
            month_name = "setembro"
        elif month == 10:
            month_name = "outubro"
        elif month == 11:
            month_name = "novembro"
        elif month == 12:
            month_name = "dezembro"

        return f"{date.day} de {month_name} de {date.year}"

    def disable_hotel_search(self):
        SEARCH_HOTEL_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/div/div/label/input"

        self.wait_clickable(5, SEARCH_HOTEL_XPATH)
        self.click(SEARCH_HOTEL_XPATH)

    def __input_itinerary(self, place: str, xpath: str, xpath_first_result: str) -> None:
        self.logger.info("Finding input box to set itinerary...")
        self.clear(xpath)
        self.send(xpath, place)
        self.click(xpath_first_result)

    def set_itineraty(self) -> None:
        self.logger.info("Setting itinerary...")
        XPATH_ORIGIN = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/input"
        XPATH_ORIGIN_FIRST_RESULT = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]"
        XPATH_DESTINATION = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/input"
        XPATH_DESTINATION_FIRST_RESULT = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]"

        self.__input_itinerary(self.origin, XPATH_ORIGIN, XPATH_ORIGIN_FIRST_RESULT)
        self.__input_itinerary(
            self.destination, XPATH_DESTINATION, XPATH_DESTINATION_FIRST_RESULT
        )
        self.logger.info("Itinerary set correctly!")

    def __input_date(self, date: datetime):
        DATE_TEMPLATE_LEFT_SIDE_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[REPLACE]/button/abbr"
        DATE_TEMPLATE_RIGHT_SIDE_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/div[REPLACE]/button/abbr"
        NEXT_PAGE_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/button[2]/span"
        continue_loop = True
        while True:
            for i in range(1, 32):
                LEFT_SIDE_XPATH = DATE_TEMPLATE_LEFT_SIDE_XPATH.replace("REPLACE", str(i))
                RIGHT_SIDE_XPATH = DATE_TEMPLATE_RIGHT_SIDE_XPATH.replace("REPLACE", str(i))
                for XPATH in [LEFT_SIDE_XPATH, RIGHT_SIDE_XPATH]:
                    try:
                        calendar_date_value = self.select(XPATH).get_attribute("aria-label")
                        print(calendar_date_value)
                        print(self.datetime_to_str_ptbr(date))
                        if calendar_date_value == self.datetime_to_str_ptbr(date):
                            continue_loop = False
                            self.click(XPATH)
                    except Exception as e:
                        print(f"Could not get the date of calendar due to: {e}")
            if continue_loop:
                self.click(NEXT_PAGE_XPATH)
            else:
                break

    def set_dates(self):
        CALENDAR_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[1]/div/div[1]"
        CLOSE_CALENDAR_BUTTON_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[2]/div/div[4]/div/button"
        SEACH_BUTTON_XPATH = "/html/body/div[1]/div[3]/div[3]/div/div/div/div/div/div[3]/div/div/div[3]/div/button"

        self.click(CALENDAR_XPATH)
        self.driver.execute_script("window.scrollTo(0, 300)")
        self.__input_date(self.departure_date_origin)
        self.__input_date(self.departure_date_destination)
        self.wait_clickable(5, CLOSE_CALENDAR_BUTTON_XPATH)
        self.click(CLOSE_CALENDAR_BUTTON_XPATH)
        self.wait_clickable(5, SEACH_BUTTON_XPATH)
        self.click(SEACH_BUTTON_XPATH)

    def crawl(self):
        self.driver.get(
            "https://www.maxmilhas.com.br/busca-passagens-aereas/RT/BHZ/SAO/2023-05-20/2023-05-24/1/0/0/EC"
        )
        # self.driver.get(self.url)
        # self.disable_hotel_search()
        # self.set_itineraty()
        # self.set_dates()
        # time.sleep(20)
        PRICE = "/html/body/div[1]/div[4]/section/div[4]/div[2]/div[1]/div/div/div[REPLACE]/div/div/div[2]/div[2]/div/div[1]/p[3]/span[2]/strong"
        time.sleep(8)
        for i in range(1, 40):
            XPATH = PRICE.replace("REPLACE", str(i))
            # self.wait_presence(15, XPATH)
            print(self.select(XPATH).text)

        # print(self.select(PRICE).text)
        # print(self.select(PRICE).text)
        # DURATION_TO_GO = "/html/body/div[1]/div[4]/section/div[4]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div/div[2]/span[1]"
        # print(self.select(DURATION_TO_GO).text)
