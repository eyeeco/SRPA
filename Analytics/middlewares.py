#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-07 21:02
# Last modified: 2017-10-08 13:59
# Filename: middlewares.py
# Description:
import time

from . import settings, backend_utils
from .models import BehaviorFlow


class AnalyticsMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request) or request
        s = time.time()
        response = self.get_response(request)
        e = time.time()
        return self.process_response(request, response, e - s) or response

    def process_request(self, request):
        pass

    @staticmethod
    def get_ip(request):
        for header in settings.IP_HEADERS:
            ip_addr = request.META.get(header, '')
            if ip_addr:
                return ip_addr.split(',')[0].strip()

    def process_response(self, request, response, render_time):
        scheme = request.scheme
        uri = request.build_absolute_uri()[:256]
        method = request.method
        referer = request.META.get('HTTP_REFERER', '')[:256]
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:256]
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

        info_dict = {
            'scheme': scheme,
            'request_uri': uri,
            'request_method': method,
            'request_referer': referer,
            'request_user_agent': user_agent,
            'request_user_id': user_id,
            'request_user_ip': user_ip,
            'response_status_code': status_code,
            'response_render_time': render_time,
        }

        for backend_name in settings.DB_BACKENDS:
            fname = 'record_to_' + backend_name
            backend = getattr(backend_utils, fname, None)
            if backend:
                backend(**info_dict)
