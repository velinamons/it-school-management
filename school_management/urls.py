from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("filias/", views.FiliaListView.as_view(), name="filias"),
    path("filias/<int:pk>/", views.FiliaDetailView.as_view(), name="filia_details"),
    path("courses/", views.CourseListView.as_view(), name="courses"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_details"),
    path("course-quiz/", views.course_quiz, name="course_quiz"),
    path("contact-with-quiz/", views.contact_with_quiz, name="contact_with_quiz"),
    path("contact-success/", views.contact_success, name="contact_success"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.register_student, name="register"),
    path(
        "dashboard/student/",
        views.StudentDashboardView.as_view(),
        name="student_dashboard",
    ),
    path(
        "dashboard/teacher/",
        views.TeacherDashboardView.as_view(),
        name="teacher_dashboard",
    ),
    path(
        "dashboard/education-manager/",
        views.EducationManagerDashboardView.as_view(),
        name="education_manager_dashboard",
    ),
    path(
        "dashboard/program-manager/",
        views.ProgramManagerDashboardView.as_view(),
        name="program_manager_dashboard",
    ),
    path(
        "dashboard/",
        views.RoleBasedDashboardView.as_view(),
        name="role_based_dashboard",
    ),
]
