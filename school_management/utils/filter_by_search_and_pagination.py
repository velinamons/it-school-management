from typing import List, Type
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet, Model, Q


def filter_by_search(
    queryset: QuerySet, search_query: str, search_fields: List[str]
) -> QuerySet:
    if search_query:
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(query)
    return queryset


def paginate_queryset(
    queryset: QuerySet, page_number: str, per_page: int = 5
) -> Page:
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def filter_by_search_and_paginate(
    search_query: str, page_number: str, model: Type[Model],
    search_fields: List[str], per_page: int = 5
) -> Page:
    queryset = model.objects.all()
    queryset = filter_by_search(queryset, search_query, search_fields)
    page_obj = paginate_queryset(queryset, page_number, per_page)
    return page_obj
