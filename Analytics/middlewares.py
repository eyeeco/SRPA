#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-07 21:02
# Last modified: 2017-10-07 21:48
# Filename: middlewares.py
# Description:
from . import settings
from .models import BehaviorFlow


class AnalyticsMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request) or request
        response = self.get_response(request)
        return self.process_response(request, response) or response

    def process_request(self, request):
        pass

    @staticmethod
    def get_ip(request):
        for header in settings.IP_HEADERS:
            ip_addr = request.META.get(header, '')
            if ip_addr:
                return ip_addr.split(',')[0].strip()

    def process_response(self, request, response):
        scheme = request.scheme
        uri = request.build_absolute_uri()[:256]
        method = request.method
        referer = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_id = request.user.id or '-1'
        status_code = response.status_code
        user_ip = self.get_ip(request)
        is_authenticated = request.user.is_authenticated()

        ignore_analytics = [
            settings.IGNORE_ANONYMOUS and not is_authenticated,
            method in settings.IGNORE_METHODS,
            status_code in settings.IGNORE_STATUSES,
            uri in settings.IGNORE_PREFIXES,
            user_ip in settings.IGNORE_IPS,
        ]

        if any(ignore_analytics):
            return response

        BehaviorFlow.objects.create(
            scheme=scheme,
            request_uri=uri,
            request_method=method,
            request_referer=referer,
            request_user_agent=user_agent,
            request_user_id=user_id,
            request_user_ip=user_ip,
            response_status_code=status_code)
