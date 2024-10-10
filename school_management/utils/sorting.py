from django.db.models import QuerySet


def apply_sorting(queryset: QuerySet, sort_option: str) -> QuerySet:
    if sort_option == "name_desc":
        return queryset.order_by("-name")
    elif sort_option == "newest":
        return queryset.order_by("-id")
    else:
        return queryset.order_by("name")
