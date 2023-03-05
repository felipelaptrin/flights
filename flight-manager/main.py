from flights_manager import FlightsManager
from models import Flights


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
            is_generic_destination=event["isGenericDestination"],
            currency=event["currency"],
        )

        fm = FlightsManager(flights)
        dates = fm.start_crawlers()

        if dates:
            print("SUCCESS")  #! DO NOT DELETE - USED DURING CI TESTS
        return {"statusCode": 200, "body": "All crawler were triggered!"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
