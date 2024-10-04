from django import template
from school_management.utils.role_checking import (
    user_is_student,
    user_is_teacher,
    user_is_education_manager,
    user_is_program_manager,
)

register = template.Library()


@register.simple_tag
def is_student(user):
    return user_is_student(user)


@register.simple_tag
def is_teacher(user):
    return user_is_teacher(user)


@register.simple_tag
def is_education_manager(user):
    return user_is_education_manager(user)


@register.simple_tag
def is_program_manager(user):
    return user_is_program_manager(user)
