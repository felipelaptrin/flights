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
            is_generic_destination=event["isGenericDestination"],
            currency=event.get("currency"),
        )
        print(f"Parsed input event => {flight}")
        google_flight_crawler = GoogleFlightsCrawler(flight)
        if flight.is_generic_destination:
            results = google_flight_crawler.crawl_generic_destinations()
        else:
            results = google_flight_crawler.crawl_specific_destination()
        if results:
            Database().store_results(results)
            print("SUCCESS")  #! DO NOT DELETE - USED DURING CI TESTS
        return {"statusCode": 200, "body": "Crawler run successfully"}
    except Exception as e:
        print(f"Something went wrong: {e}")
        return {"statusCode": 500, "body": f"Something went wrong: {str(e)}"}
