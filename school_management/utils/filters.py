import django_filters
from django.forms.widgets import CheckboxSelectMultiple
from school_management.models import Course, Experience, Filia, Group
from school_management.utils.enums import AgeGroup, GroupStatus


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

    age_group = django_filters.MultipleChoiceFilter(
        field_name="age_group",
        choices=AgeGroup.choices(),
        label="Age Group",
        widget=CheckboxSelectMultiple(),
    )

    class Meta:
        model = Course
        fields = ["experience", "filia", "age_group"]


class GroupFilter(django_filters.FilterSet):
    filia = django_filters.ModelMultipleChoiceFilter(
        field_name="filia",
        queryset=Filia.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="Filia",
        conjoined=False,
    )
    course = django_filters.ModelMultipleChoiceFilter(
        field_name="course",
        queryset=Course.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="Course",
        conjoined=False,
    )

    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=GroupStatus.choices(),
        widget=CheckboxSelectMultiple(),
        label="Status",
    )

    class Meta:
        model = Group
        fields = ["filia", "course", "status"]
