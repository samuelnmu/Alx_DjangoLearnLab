# LibraryProject/middleware.py
from django.utils.deprecation import MiddlewareMixin

class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' cdn.jsdelivr.net; style-src 'self' fonts.googleapis.com"
        return response
