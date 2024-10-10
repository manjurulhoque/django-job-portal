from prometheus_client import Counter, Enum, Gauge, Histogram, Info, Summary

info = Info(name="app", documentation="Information about the application")
info.info({"version": "1.0", "language": "python", "framework": "django"})

requests_total = Counter(
    name="app_requests_total",
    documentation="Total number of various requests.",
    labelnames=["endpoint", "method", "user"],
)
last_user_activity_time = Gauge(
    name="app_last_user_activity_time_seconds",
    documentation="The last time when user was active.",
    labelnames=["user"],
)

response_time_histogram = Histogram(
    name="app_response_time_seconds", documentation="Response time for requests", labelnames=["method", "endpoint"]
)

error_rates_counter = Counter(
    name="app_error_rates_total", documentation="The total number of errors", labelnames=["status_code", "endpoint"]
)
