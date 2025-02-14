from pydantic import BaseModel


class TimeZones(BaseModel):
    timezones: dict[str, str]
