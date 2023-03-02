import json
import logging
import os
from datetime import datetime, timedelta
from logging import Logger
from typing import List, Tuple

import boto3
from config import AWS_REGION, CRAWLER_LAMBDA_NAME, DRY_RUN, LOGGER_LEVEL, MAX_CRAWLERS
from models import Flights


class FlightsManager:
    def __init__(
        self,
        flights: Flights,
    ):
        self.min_departure_date_origin = flights.min_departure_date_origin
        self.max_departure_date_destination = flights.max_departure_date_destination
        self.min_stay_days = flights.min_stay_days
        self.max_stay_days = flights.max_stay_days
        self.origin = flights.origin
        self.destination = flights.destination
        self.__logger_level = LOGGER_LEVEL
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
        self.logger.debug(
            f"Possible travel dates retrieved sucessfully! {len(possible_dates)} possible travel dates retrieved!"
        )
        return possible_dates

    def trigger_crawler(self, departure_date_origin: str, departure_date_destination: str):
        lambda_client = boto3.client("lambda", region_name=AWS_REGION)
        payload = bytes(
            json.dumps(
                {
                    "departureDateOrigin": self.__serialize_datetime(departure_date_origin),
                    "departureDateDestination": self.__serialize_datetime(
                        departure_date_destination
                    ),
                    "origin": self.origin,
                    "destination": self.destination,
                },
            ),
            encoding="utf8",
        )
        try:
            success_message = f"Triggered crawer on dates {departure_date_origin}-{departure_date_destination}"
            if DRY_RUN == "TRUE":
                self.logger.info(f"[DRY RUN] {success_message}")
            else:
                lambda_client.invoke(
                    FunctionName=CRAWLER_LAMBDA_NAME, InvocationType="Event", Payload=payload
                )
                self.logger.info(success_message)
        except Exception as e:
            self.logger.error("Could not trigger AWS Lambda crawler due to: {e}")

    def start_crawlers(self):
        self.logger.info("Started to trigger lambdas to start to crawl the pages...")
        possible_travel_dates = self.get_possible_travel_dates()

        if len(possible_travel_dates) > MAX_CRAWLERS:
            error_message = f"The number of pages to crawl is too high ({len(possible_travel_dates)}). Please set 'MAX_CRAWLERS' accordingly."
            self.logger.error(error_message)
            raise Exception(error_message)

        for possible_travel_date in possible_travel_dates:
            self.trigger_crawler(possible_travel_date[0], possible_travel_date[1])

    def __serialize_datetime(self, date: datetime) -> str:
        return date.strftime("%d/%m/%Y")


def handler(event=None, context=None):
    print(f"Input event: {event}")
    try:
        flights = Flights(
            min_departure_date_origin=event["minDepartureDateOrigin"],
            max_departure_date_destination=event["maxDepartureDateDestination"],
            origin=event["origin"],
            destination=event["destination"],
            min_stay_days=event["minStayDays"],
            max_stay_days=event["maxStayDays"],
        )

        fm = FlightsManager(flights)
        fm.start_crawlers()
        return {"statusCode": 200, "body": "All crawler were triggered!"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
