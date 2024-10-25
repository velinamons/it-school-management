from typing import Any


def user_is_student(user: Any) -> bool:
    return hasattr(user, "student")


def user_is_teacher(user: Any) -> bool:
    return hasattr(user, "teacher")


def user_is_student_or_teacher(user: Any) -> bool:
    return hasattr(user, "teacher") or hasattr(user, "student")


def user_is_education_manager(user: Any) -> bool:
    return hasattr(user, "manager") and user.manager.role == "Education"


def user_is_program_manager(user: Any) -> bool:
    return hasattr(user, "manager") and user.manager.role == "Program"


def get_user_role(user: Any) -> str | None:
    if user_is_student(user):
        return "student"
    elif user_is_teacher(user):
        return "teacher"
    elif user_is_education_manager(user):
        return "education_manager"
    elif user_is_program_manager(user):
        return "program_manager"
    return None
