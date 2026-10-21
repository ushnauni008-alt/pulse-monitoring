
from unittest.mock import patch
from ssl_check import check_ssl_certificate

with patch(
    "ssl_check.socket.create_connection",
    side_effect=TimeoutError("Connection timed out")
):
    result = check_ssl_certificate("example.com")

print(result)
