import logging
import os
from logging import Logger
from typing import List

from config import (
    CLUSTER_ID,
    DATABASE_SECRET_NAME,
    DB_CLUSTER,
    DB_COLLECTION,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
    LOGGER_LEVEL,
)
from pymongo import MongoClient
from utils import get_secret


class Database:
    def __init__(self):
        self.__logger_level = LOGGER_LEVEL
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
        if DATABASE_SECRET_NAME:
            get_secret(DATABASE_SECRET_NAME)
        print(os.getenv("DATABASE_SECRET_NAME"))
        user = DB_USER
        print(os.getenv("DB_USER"))
        print(user)
        password = DB_PASSWORD
        db_name = DB_NAME
        cluster_name = DB_CLUSTER
        cluster_id = CLUSTER_ID
        collection_name = DB_COLLECTION
        try:
            db_connection_string = f"mongodb+srv://{user}:{password}@{cluster_name}.{cluster_id}.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(db_connection_string)
            db = client[db_name]
            collection = db[collection_name]
        except Exception as e:
            self.logger.error("Could not stablish a connection with the database")
            raise Exception(f"Could not connect to DB due to the following error: {e}")

        return collection

    def store_results(
        self,
        documents: List[dict],
    ) -> None:
        self.collection.insert_many(documents)
        self.logger.info("Crawled dates saved in the Database!")


Database().store_results(
    [
        {
            {
                "destination": "Phnom Penh",
                "duration": 29.166666666666668,
                "stops": 2,
                "price": 7515,
                "currency": "R$",
                "id": "05032023192546506331",
                "stay_days": 15,
                "departure_date_origin": "10/09/2023",
                "departure_date_destination": "25/09/2023",
            }
        }
    ]
)
