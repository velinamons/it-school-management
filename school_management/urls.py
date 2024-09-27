from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("locations/", views.locations, name="locations"),
    path("courses/", views.courses, name="courses"),
    path("course-quiz/", views.course_quiz, name="course_quiz"),
    path("contact/", views.contact, name="contact"),
    path("contact-with-quiz/", views.contact_with_quiz, name="contact_with_quiz"),
    path("contact-success/", views.contact_success, name="contact_success"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]
