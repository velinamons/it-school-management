from functools import wraps
from typing import Callable, Any
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
import logging
from school_management.utils.error_views import custom_401

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

ViewFunction = Callable[[HttpRequest, Any, Any], HttpResponse]


def login_required_401(view_func: ViewFunction) -> ViewFunction:
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return custom_401(request)
        return view_func(request, *args, **kwargs)

    return wrapped_view


def user_passes_test_403(
    test_func: Callable[[Any], bool]
) -> Callable[[ViewFunction], ViewFunction]:
    def decorator(view_func: ViewFunction) -> ViewFunction:
        @wraps(view_func)
        def wrapped_view(
            request: HttpRequest, *args: Any, **kwargs: Any
        ) -> HttpResponse:
            if not test_func(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def exception_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in {func.__name__}: {e}")
            return False
    return wrapper
