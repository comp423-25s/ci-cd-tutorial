"""FastAPI main entrypoint file."""

from fastapi import FastAPI, Depends
from typing import Annotated
from models import TimeZones
from services import TimezoneService

app = FastAPI()


TIMEZONES = [
    "America/New_York",
    "Africa/Johannesburg",
]


@app.get("/")
def main(time_service: Annotated[TimezoneService, Depends()]) -> TimeZones:
    return time_service.get_current_times_in_timezones(TIMEZONES)
