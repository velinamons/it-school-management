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
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]
