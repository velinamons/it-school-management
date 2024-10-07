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
    path("logout/", views.logout_view, name="logout"),
    path(
        "dashboard/",
        views.RoleBasedDashboardView.as_view(),
        name="role_based_dashboard",
    ),
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
        "dashboard/program-manager/manage_courses/",
        views.ManageCoursesView.as_view(),
        name="program_manage_courses",
    ),
    path(
        "dashboard/program-manager/manage_courses/<int:pk>/change/",
        views.ManageCourseChangeView.as_view(),
        name="program_change_course",
    ),
    path(
        "dashboard/program-manager/manage_courses/add/",
        views.ManageCourseAddView.as_view(),
        name="program_add_course",
    ),
    path(
        "dashboard/program-manager/manage_courses/<int:pk>/delete/",
        views.ManageCourseDeleteView.as_view(),
        name="program_delete_course",
    ),
    path(
        "dashboard/program-manager/manage_groups/",
        views.ProgramManageGroupsView.as_view(),
        name="program_manage_groups",
    ),
    path(
        "dashboard/program-manager/manage_groups/add/",
        views.ManageGroupAddView.as_view(),
        name="program_add_group",
    ),
    path(
        "dashboard/program-manager/manage_groups/<int:pk>/change/",
        views.ProgramManageGroupChangeView.as_view(),
        name="program_change_group",
    ),
    path(
        "dashboard/program-manager/manage_groups/<int:pk>/delete/",
        views.ManageGroupDeleteView.as_view(),
        name="program_delete_group",
    ),
    path(
        "operation_success/<str:operation_type>/<str:object_name>/<path:back_url>/",
        views.OperationSuccessView.as_view(),
        name="operation_success",
    ),
    path(
        "dashboard/education-manager/manage_groups/",
        views.EducationManageGroupsView.as_view(),
        name="education_manage_groups",
    ),
    path(
        "dashboard/education-manager/manage_groups/<int:pk>/",
        views.EducationManageGroupDetailsView.as_view(),
        name="education_manage_group_details",
    ),
    path(
        "dashboard/education-manager/manage_groups/<int:pk>/add_teachers/",
        views.EducationManageGroupAddTeachersView.as_view(),
        name="education_add_teachers_to_group",
    ),
    path(
        "dashboard/education-manager/manage_groups/<int:pk>/add_students/",
        views.EducationManageGroupAddStudentsView.as_view(),
        name="education_add_students_to_group",
    ),
]
