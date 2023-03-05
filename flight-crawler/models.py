from datetime import datetime
from typing import Optional

from config import DATE_FORMAT
from pydantic import BaseModel, validator


class Flights(BaseModel):
    departure_date_destination: datetime
    departure_date_origin: datetime
    origin: str
    destination: str
    is_generic_destination: bool
    currency: Optional[str] = "USD"

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
            raise Exception("departureDateOrigin can't be before than departureDateDestination")
        return v

    @validator("isGenericDestination", pre=True, check_fields=False)
    def validate_generic_destination(cls, v):
        if isinstance(v) == str:
            value = True if v.upper() == "TRUE" else False
        elif isinstance(v) == bool:
            return v
        else:
            raise Exception("isGenericDestination must be a boolean!")

    @validator("currency")
    def validate_currency(cls, v):
        currency = v.strip()
        if len(currency) != 3:
            raise Exception(
                f"Currency '{currency}' is not a valid currency! It must be 3 letters long (e.g. USD, EUR)"
            )
        return currency.upper()
