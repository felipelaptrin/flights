from datetime import datetime

from config import DATE_FORMAT
from pydantic import BaseModel, validator
from pydantic.types import PositiveInt


class Flights(BaseModel):
    max_departure_date_destination: datetime
    min_departure_date_origin: datetime
    origin: str
    destination: str
    min_stay_days: PositiveInt
    max_stay_days: PositiveInt
    is_generic_destination: bool

    @validator(
        "min_departure_date_origin",
        "max_departure_date_destination",
        pre=True,
        check_fields=False,
    )
    def validate_date(cls, v):
        parsed = datetime.strptime(v, DATE_FORMAT)
        return parsed

    @validator(
        "min_departure_date_origin",
        check_fields=False,
    )
    def validate_range_date(cls, v, values):
        if v > values["max_departure_date_destination"]:
            raise Exception(
                "minDepartureDateOrigin can't be before than maxDepartureDateDestination"
            )
        return v

    @validator("max_stay_days")
    def validate_range_stay(cls, v, values):
        if v < values["min_stay_days"]:
            raise Exception("minStayDays must be higher than maxStayDays")
        return v
