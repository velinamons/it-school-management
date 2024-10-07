from functools import wraps
from typing import Callable, Any
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import PermissionDenied
from school_management.utils.error_views import custom_401

ViewFunction = Callable[[HttpRequest, Any, Any], HttpResponse]


def login_required_401(view_func: ViewFunction) -> ViewFunction:
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return custom_401(request)
        return view_func(request, *args, **kwargs)
    return wrapped_view


def user_passes_test_403(test_func: Callable[[Any], bool]) -> Callable[[ViewFunction], ViewFunction]:
    def decorator(view_func: ViewFunction) -> ViewFunction:
        @wraps(view_func)
        def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not test_func(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
