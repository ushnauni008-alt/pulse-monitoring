
import ssl
import socket
from datetime import datetime, timezone

SSL_WARNING_DAYS = 30

def check_ssl_certificate(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(
            sock, server_hostname=hostname
            ) as secure_sock:
                certificate = secure_sock.getpeercert()

    except ssl.SSLCertVerificationError as error:
        return {
            "website": hostname,
            "ssl_status": "CERTIFICATE ERROR",
            "error": str(error)
        }


    except socket.gaierror as error:
        return {
            "website": hostname,
            "ssl_status": "DNS ERROR",
            "error": str(error)
        }

    except (socket.timeout, TimeoutError) as error:
        return {
            "website": hostname,
            "ssl_status": "CONNECTION TIMEOUT",
            "error": str(error)
        }

    except ConnectionRefusedError as error:
        return {
            "website": hostname,
            "ssl_status": "CONNECTION REFUSED",
            "error": str(error)
        }

    except ssl.SSLError as error:
        return {
            "website": hostname,
            "ssl_status": "TLS ERROR",
            "error": str(error)
        }


    expiry_text = certificate["notAfter"]

    expiry_timestamp = ssl.cert_time_to_seconds(expiry_text)

    expiry_date = datetime.fromtimestamp(
        expiry_timestamp, timezone.utc
    )

    remaining = expiry_date - datetime.now(timezone.utc)

    days_left = remaining.days

    if remaining.total_seconds() <= 0:
       ssl_status = "EXPIRED"
    elif remaining.total_seconds() <= SSL_WARNING_DAYS * 24 * 60 * 60:
       ssl_status = "EXPIRING SOON"
    else:
      ssl_status = "VALID"

    return {
        "website": hostname,
        "expiry_date": expiry_date.isoformat(),
        "days_remaining": days_left,
        "ssl_status": ssl_status,
        "warning_threshold_days": SSL_WARNING_DAYS
    }
if __name__ == "__main__":
    print(check_ssl_certificate("example.com"))
