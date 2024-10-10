from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render


def custom_404(request: HttpRequest, exception: Http404) -> HttpResponse:
    return render(request, "errors/404.html", status=404)


def custom_500(request: HttpRequest) -> HttpResponse:
    return render(request, "errors/500.html", status=500)


def custom_401(request: HttpRequest) -> HttpResponse:
    return render(request, "errors/401.html", status=401)


def custom_403(request: HttpRequest, exception: None) -> HttpResponse:
    return render(request, "errors/403.html", status=403)
