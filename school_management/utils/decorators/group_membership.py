from functools import wraps
from typing import Callable, Any
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from school_management.models import Group
from django.core.exceptions import PermissionDenied

ViewFunction = Callable[[HttpRequest, Any, Any], HttpResponse]


def student_in_group(view_func: ViewFunction) -> ViewFunction:
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        group = get_object_or_404(Group, pk=kwargs["pk"])
        if not (hasattr(request.user, "student") and group.students.filter(id=request.user.student.id).exists()):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view


def teacher_in_group(view_func: ViewFunction) -> ViewFunction:
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        group = get_object_or_404(Group, pk=kwargs["pk"])
        if not (hasattr(request.user, "teachers") and group.teachers.filter(id=request.user.teacher.id).exists()):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view
