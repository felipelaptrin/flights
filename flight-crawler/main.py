from config import GENERIC_DESTINATION
from database import Database
from google_flights import GoogleFlightsCrawler
from models import Flights


def handler(event=None, context=None):
    print(f"Input event => {event}")
    try:
        flight = Flights(
            departure_date_origin=event["departureDateOrigin"],
            departure_date_destination=event["departureDateDestination"],
            origin=event["origin"],
            destination=event["destination"],
        )
        google_flight_crawler = GoogleFlightsCrawler(flight)
        if GENERIC_DESTINATION:
            results = google_flight_crawler.crawl_generic_destinations()
            if results:
                Database().store_results(results)
        else:
            raise NotImplementedError("Not implemented yet!")

        print("SUCCESS")  #! DO NOT DELETE - USED DURING CI TESTS
        return {"statusCode": 200, "body": "Crawler run successfully"}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": f"Something went wrong: {str(e)}"}


handler(
    {
        "departureDateOrigin": "03/03/2023",
        "departureDateDestination": "10/03/2023",
        "origin": "Boston",
        "destination": "Asia",
    },
    "",
)
