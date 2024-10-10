import time

from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from jobsapp.metrics import error_rates_counter, requests_total, last_user_activity_time, response_time_histogram


class CustomMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        # Exclude metrics endpoint from processing
        if "metrics" not in request.path:
            # Increment the Prometheus counter
            requests_total.labels(
                endpoint=request.get_full_path(),  # call the method to get the path
                method=request.method,
                user=request.user.get_username() if request.user.is_authenticated else "Anonymous",
                # use get_username() for the user label
            ).inc()

            # Update the last user activity time
            if request.user.is_authenticated:
                last_user_activity_time.labels(user=request.user.get_username()).set(now().timestamp())

        # Call the next middleware or view
        response = self.get_response(request)
        return response


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        response_time = time.time() - start_time

        response_time_histogram.labels(method=request.method, endpoint=request.path).observe(response_time)

        return response


class ErrorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 400 <= response.status_code < 600:
            error_rates_counter.labels(status_code=response.status_code, endpoint=request.path).inc()
        return response
