from datetime import datetime
import pytz
from models import TimeZones  # import the model


class TimezoneService:
    def get_current_times_in_timezones(self, timezones: list[str]) -> TimeZones:
        tz_dict = {}
        utc_now = datetime.now(pytz.utc)
        for tz in timezones:
            timezone = pytz.timezone(tz)
            tz_time = utc_now.astimezone(timezone)
            formatted_time = tz_time.strftime("%I:%M %p").lstrip("0")
            if tz_time.date() > utc_now.date():
                formatted_time += " (next day)"
            tz_dict[tz] = formatted_time
        return TimeZones(timezones=tz_dict)
