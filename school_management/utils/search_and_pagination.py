from typing import Tuple, List
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet, Model, Q
from django.http import HttpRequest


def search(
    request: HttpRequest, queryset: QuerySet, search_fields: List[str]
) -> Tuple[QuerySet, str]:
    search_query = request.GET.get("q", "")
    if search_query:
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(query)
    return queryset, search_query


def paginate(request: HttpRequest, queryset: QuerySet, per_page: int = 5) -> Page:
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def search_and_paginate(
    request: HttpRequest, model, search_fields: List[str], per_page: int = 5
) -> Tuple[Page, str]:
    queryset = model.objects.all()
    queryset, search_query = search(request, queryset, search_fields)
    page_obj = paginate(request, queryset, per_page)
    return page_obj, search_query
