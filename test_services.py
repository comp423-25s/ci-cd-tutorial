import re
from services import TimezoneService
from models import TimeZones


def test_get_current_times_in_timezones_with_valid_input():
    # Given: a list of known timezones and a TimezoneService instance
    timezones = ["Africa/Johannesburg", "America/New_York"]
    service = TimezoneService()

    # When: retrieving current times for the provided timezones
    result: TimeZones = service.get_current_times_in_timezones(timezones)

    # Then: the result should be an instance of TimeZones containing the provided keys
    assert isinstance(result, TimeZones), "Expected result to be a TimeZones model"
    assert set(result.timezones.keys()) == set(
        timezones
    ), "Returned keys do not match the input list"

    # And: each time string should match the expected format (e.g., "H:MM AM/PM" with optional " (next day)")
    pattern = re.compile(r"^\d{1,2}:\d{2} (AM|PM)( \(next day\))?$")
    for tz, time_str in result.timezones.items():
        assert pattern.match(
            time_str
        ), f"Time string '{time_str}' for timezone '{tz}' does not match expected format"


def test_get_current_times_in_timezones_with_empty_input():
    # Given: an empty list of timezones and a TimezoneService instance
    service = TimezoneService()

    # When: retrieving current times for an empty timezone list
    result: TimeZones = service.get_current_times_in_timezones([])

    # Then: the result should be an instance of TimeZones with an empty dictionary
    assert isinstance(result, TimeZones), "Expected result to be a TimeZones model"
    assert (
        result.timezones == {}
    ), "Expected empty dictionary when input timezone list is empty"
