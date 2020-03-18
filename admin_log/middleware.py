from typing import Optional

from django.http import HttpRequest
from django.utils.decorators import classproperty


class AdminLogMiddleware:
    request: Optional[HttpRequest]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            self.request_started(request)
            response = self.get_response(request)
        finally:
            self.request_finished(request)
        return response

    @classmethod
    def get_user_id(cls) -> Optional[int]:
        request = getattr(cls, 'request', None)
        if request is None:
            return None
        if request.user.is_authenticated and request.user.is_staff:
            return request.user.pk
        return None

    def request_started(self, request):
        self.__class__.request = request

    # noinspection PyUnusedLocal
    def request_finished(self, request):
        self.__class__.request = None
