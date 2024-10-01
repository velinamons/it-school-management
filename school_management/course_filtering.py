from django.db.models import QuerySet
from .models import Course


def filter_courses_by_age(
    courses_list: QuerySet[Course], age_group: str
) -> QuerySet[Course]:
    return courses_list.filter(age_group=age_group)


def filter_courses_by_experience(
    courses_list: QuerySet[Course], experience_name: str
) -> QuerySet[Course]:
    return courses_list.filter(experience__name=experience_name)


def filter_courses_by_goals(
    courses_list: QuerySet[Course], learning_goals: list[str]
) -> QuerySet[Course]:
    return courses_list.filter(goals__name__in=learning_goals).distinct()


def select_course(
    age_group: str, experience_name: str, learning_goals: list[str]
) -> None | Course:
    courses_list = Course.objects.all()
    age_filtered_courses = filter_courses_by_age(courses_list, age_group)
    experience_filtered_courses = filter_courses_by_experience(
        age_filtered_courses, experience_name
    )
    goal_matched_courses = filter_courses_by_goals(
        experience_filtered_courses, learning_goals
    )

    if goal_matched_courses.exists():
        return goal_matched_courses.first()
    return None
