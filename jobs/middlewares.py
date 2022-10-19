from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from jobsapp.metrics import requests_total, last_user_activity_time


class CustomMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        path = request.path
        user = request.user
        if "metrics" not in path:
            # because metrics is for prometheus url
            requests_total.labels(
                endpoint=request.get_full_path, method=request.method, user=user
            ).inc()
        last_user_activity_time.labels(user=user).set(now().timestamp())
