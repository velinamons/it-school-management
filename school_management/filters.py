import django_filters
from django.forms.widgets import CheckboxSelectMultiple
from .models import Course, Experience, Filia


class CourseFilter(django_filters.FilterSet):
    experience = django_filters.ModelMultipleChoiceFilter(
        field_name="experience",
        queryset=Experience.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="Experience",
        conjoined=False,
    )
    filia = django_filters.ModelMultipleChoiceFilter(
        field_name="groups__filia",
        queryset=Filia.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="Filia",
        conjoined=False,
    )

    class Meta:
        model = Course
        fields = ["experience", "filia"]
