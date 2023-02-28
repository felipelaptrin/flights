import json
import logging
import os
from datetime import datetime, timedelta
from logging import Logger
from typing import List, Tuple

import boto3

DATE_FORMAT = "%d/%m/%Y"


class FlightsManager:
    def __init__(
        self,
        origin: str,
        destination: str,
        min_departure_date_origin: str,
        max_departure_date_destination: str,
        min_stay_days: int,
        max_stay_days: int,
    ):
        self.min_departure_date_origin = datetime.strptime(
            min_departure_date_origin, DATE_FORMAT
        )
        self.max_departure_date_destination = datetime.strptime(
            max_departure_date_destination, DATE_FORMAT
        )
        self.min_stay_days = min_stay_days
        self.max_stay_days = max_stay_days
        self.origin = origin
        self.destination = destination
        self.__logger_level = os.getenv("LOGGER_LEVEL", "INFO")
        self.logger = self.__get_logger()

    def __get_logger(self) -> Logger:
        logger = logging.getLogger()
        logger.setLevel(self.__logger_level)
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s: %(message)s", level=self.__logger_level
        )

        return logger

    def get_possible_travel_dates(self) -> List[Tuple[datetime, datetime]]:
        self.logger.debug("Retrieving the possible travel dates...")
        possible_dates = []
        available_period_for_travel = (
            self.max_departure_date_destination - self.min_departure_date_origin
        ).days
        for i in range(available_period_for_travel):
            possible_departure_date_origin = self.min_departure_date_origin + timedelta(days=i)

            stay_days_range = self.max_stay_days - self.min_stay_days + 1
            for j in range(stay_days_range):
                stay_days = self.min_stay_days + j
                possible_departure_date_destination = (
                    possible_departure_date_origin + timedelta(days=stay_days - 1)
                )
                if possible_departure_date_destination > self.max_departure_date_destination:
                    continue
                possible_dates.append(
                    (possible_departure_date_origin, possible_departure_date_destination)
                )
        return possible_dates

    def start_crawlers(self):
        self.logger.info("Started to trigger lambdas to start to crawl the pages...")
        possible_travel_dates = self.get_possible_travel_dates()
        if len(possible_travel_dates) > int(os.getenv("MAX_POSSIBLE_DATES", 100)):
            error_message = f"The number of pages to crawl is too high ({len(possible_travel_dates)}). Please set 'MAX_POSSIBLE_DATES' accordingly."
            self.logger.error(error_message)
            raise Exception(error_message)
        for possible_travel_date in possible_travel_dates:
            lambda_client = boto3.client("lambda", region_name=os.getenv("AWS_REGION"))
            response = lambda_client.invoke(
                FunctionName=os.getenv("CRAWLER_LAMBDA_NAME"),
                InvocationType="Event",
                Payload=bytes(
                    json.dumps(
                        {
                            "departureDateOrigin": self.__serialize_datetime(
                                possible_travel_date[0]
                            ),
                            "departureDateDestination": self.__serialize_datetime(
                                possible_travel_date[1]
                            ),
                            "origin": self.origin,
                            "destination": self.destination,
                        },
                    ),
                    encoding="utf8",
                ),
            )
            print(response)

    def __serialize_datetime(self, date: datetime) -> str:
        return date.strftime("%d/%m/%Y")


def handler(event=None, context=None):
    min_departure_date_origin = event["minDepartureDateOrigin"]
    max_departure_date_destination = event["maxDepartureDateDestination"]
    origin = event["origin"]
    destination = event["destination"]
    min_stay_days = event["minStayDays"]
    max_stay_days = event["maxStayDays"]

    fm = FlightsManager(
        origin,
        destination,
        min_departure_date_origin,
        max_departure_date_destination,
        min_stay_days,
        max_stay_days,
    )
    if os.getenv("RUN_LOCALLY", "FALSE").upper() == "FALSE":
        fm.start_crawlers()
        return {"statusCode": 200, "body": "Crawler run successfully"}
    else:
        flights = fm.get_possible_travel_dates()
        flights_parsed = []
        for flight in flights:
            flights_parsed.append(
                {
                    "initialDate": flight[0].strftime("%d/%m/%Y"),
                    "finalDate": flight[1].strftime("%d/%m/%Y"),
                }
            )
        return {"statusCode": 200, "body": "Crawler run successfully", "data": flights_parsed}
