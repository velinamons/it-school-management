from django.core.paginator import Paginator
from django.db.models import Q


def search_and_paginate(request, model, search_fields):
    search_query = request.GET.get("q", "")
    queryset = model.objects.all()

    if search_query:
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(query)

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj, search_query
