from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("locations/", views.locations, name="locations"),
    path("courses/", views.courses, name="courses"),
    path("faq/", views.faq, name="faq"),
    path('course-quiz/', views.course_quiz, name='course_quiz'),
    path('course-quiz-result/', views.course_quiz_result, name='course_quiz_result'),
]
