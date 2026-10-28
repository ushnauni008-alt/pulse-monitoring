from fastapi import FastAPI
import httpx
import time
from ssl_check import check_ssl_certificate

app = FastAPI()
RESPONSE_TIME_THRESHOLD_MS = 1000

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "Welcome to Pulse Monitoring Application"}

@app.get("/check")
def check_website():
    hostname = "example.com"
    return perform_http_check(hostname)

def perform_http_check(hostname):
    url = f"https://{hostname}"

    try:
        start_time = time.perf_counter()

        response = httpx.get(url, timeout=10.0)

        end_time = time.perf_counter()

        response_time = round(
            (end_time - start_time) * 1000, 2
        )
        if response.status_code >= 400:
           website_status = "DOWN"
        elif response_time > RESPONSE_TIME_THRESHOLD_MS:
            website_status = "SLOW"
        else:
            website_status = "UP"

        return {
            "website": url,
            "status": website_status,
            "http_status": response.status_code,
            "response_time_ms": response_time,
            "threshold_ms": RESPONSE_TIME_THRESHOLD_MS
        }

    except httpx.RequestError as error:
        return {
            "website": url,
            "status": "DOWN",
            "error": str(error)
        }

@app.get("/ssl-check")
def ssl_check():
    hostname = "example.com"

    result = check_ssl_certificate(hostname)

    return result

from fastapi import Query, HTTPException

ALLOWED_WEBSITES = {
    "example": "example.com",
    "python": "www.python.org"
}

@app.get("/monitor")
def monitor_website(site: str = Query(default="example")):
    if site not in ALLOWED_WEBSITES:
        raise HTTPException(
           status_code=400,
           detail="Website not allowed"
        )


    hostname = ALLOWED_WEBSITES[site]

    http_result = perform_http_check(hostname)

    ssl_result = check_ssl_certificate(hostname)

    return {
        "website": hostname,
        "http_monitoring": http_result,
        "ssl_monitoring": ssl_result
    }
