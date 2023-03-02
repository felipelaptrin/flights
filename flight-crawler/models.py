from datetime import datetime

from config import DATE_FORMAT
from pydantic import BaseModel, validator


class Flights(BaseModel):
    departure_date_destination: datetime
    departure_date_origin: datetime
    origin: str
    destination: str

    @validator(
        "departure_date_origin",
        "departure_date_destination",
        pre=True,
        check_fields=False,
    )
    def validate_date(cls, v):
        parsed = datetime.strptime(v, DATE_FORMAT)
        return parsed

    @validator(
        "departure_date_origin",
        check_fields=False,
    )
    def validate_range_date(cls, v, values):
        if v > values["departure_date_destination"]:
            raise Exception(
                "departureDateOrigin can't be before than departureDateDestination"
            )
        return v
