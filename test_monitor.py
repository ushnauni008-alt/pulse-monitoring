
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_monitor_example():

    fake_http = {
        "website": "https://example.com",
        "status": "UP",
        "http_status": 200,
        "response_time_ms": 150,
        "threshold_ms": 1000
    }

    fake_ssl = {
        "website": "example.com",
        "ssl_status": "VALID",
        "days_remaining": 70
    }

    with patch("main.perform_http_check", return_value=fake_http), \
         patch("main.check_ssl_certificate", return_value=fake_ssl):

        response = client.get("/monitor?site=example")

    assert response.status_code == 200

    data = response.json()

    assert data["website"] == "example.com"
    assert data["http_monitoring"]["status"] == "UP"
    assert data["ssl_monitoring"]["ssl_status"] == "VALID"


def test_monitor_rejects_unknown_website():

    with patch("main.perform_http_check") as mock_http, \
         patch("main.check_ssl_certificate") as mock_ssl:

        response = client.get("/monitor?site=unknown")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Website not allowed"

    mock_http.assert_not_called()
    mock_ssl.assert_not_called()


@pytest.mark.parametrize("site", [
    "unknown",
    "internal",
    "google",
    "admin"
])
def test_reject_multiple_invalid_sites(site):
    with patch("main.perform_http_check") as mock_http, \
         patch("main.check_ssl_certificate") as mock_ssl:

         response = client.get(f"/monitor?site={site}")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Website not allowed"

    mock_http.assert_not_called()
    mock_ssl.assert_not_called()