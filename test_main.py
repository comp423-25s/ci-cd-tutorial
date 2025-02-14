from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_main():
    # Given: A running FastAPI app and test client
    # When: Sending a GET request to the "/" endpoint
    response = client.get("/")

    # Then: The response status code should be 200
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()

    # And Given: The response contains a "timezones" key with a dictionary value
    assert "timezones" in data, "Expected key 'timezones' in response"
    assert isinstance(
        data["timezones"], dict
    ), "Expected 'timezones' to be a dictionary"

    # Then: Each expected timezone should be present in the response
    expected_timezones = ["Africa/Johannesburg", "America/New_York"]
    for tz in expected_timezones:
        assert tz in data["timezones"], f"Expected timezone {tz} in response"
