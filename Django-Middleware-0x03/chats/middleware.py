#!/usr/bin/env python3

from datetime import datetime
import logging
from django.http import HttpResponseForbidden

# Configure the logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server hour (0–23)
        current_hour = datetime.now().hour

        # Restrict access if NOT between 18 (6PM) and 21 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 6PM and 9PM."
                )

        response = self.get_response(request)
        return response
