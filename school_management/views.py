from typing import Any, Dict
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    UpdateView,
    DeleteView,
    CreateView,
    View,
)
from django_filters.views import FilterView
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import Course, Filia, Group, Student, Teacher
from school_management.utils.filters import CourseFilter, GroupFilter
from school_management.utils.course_filtering import select_course
from .forms import (
    StudentRegistrationForm,
    CustomAuthenticationForm,
    SuggestionForm,
    ContactForm,
    CourseForm,
    GroupForm,
)
from school_management.utils.role_checking import (
    user_is_student,
    user_is_teacher,
    user_is_program_manager,
    user_is_education_manager,
    get_user_role,
)
from .utils.sorting import apply_sorting
from .utils.views_decorators import login_required_401, user_passes_test_403


def home(request: HttpRequest) -> HttpResponse:
    courses = Course.objects.all().order_by("name")[:3]

    context = {"courses": courses}

    return render(request, "unauthorized/home.html", context)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "registration/login.html"

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        remember = form.cleaned_data.get("remember")
        if not remember:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("role_based_dashboard")


def register_student(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = StudentRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required_401
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        logout(request)
        return redirect("home")

    return render(request, "registration/logout_confirmation.html")


@method_decorator([login_required_401], name="dispatch")
class RoleBasedDashboardView(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        role = get_user_role(user)

        if role:
            return redirect(f"{role}_dashboard")

        return redirect("home")


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_student)], name="dispatch"
)
class StudentDashboardView(TemplateView):
    template_name = "dashboard/student_dashboard.html"


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_teacher)], name="dispatch"
)
class TeacherDashboardView(TemplateView):
    template_name = "dashboard/teacher_dashboard.html"


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_education_manager)],
    name="dispatch",
)
class EducationManagerDashboardView(TemplateView):
    template_name = "dashboard/education_manager_dashboard.html"


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ProgramManagerDashboardView(TemplateView):
    template_name = "dashboard/program_manager_dashboard.html"


@method_decorator([login_required_401], name="dispatch")
class OperationSuccessView(View):
    def get(
        self,
        request: HttpRequest,
        operation_type: str,
        object_name: str,
        back_url: str,
        *args,
        **kwargs,
    ) -> HttpResponse:
        context = {
            "operation_type": operation_type,
            "object_name": object_name,
            "back_url": back_url,
        }
        return render(request, "managers/operation_success.html", context)


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageCoursesView(FilterView):
    template_name = "managers/program_manage_courses.html"
    context_object_name = "courses"
    filterset_class = CourseFilter
    paginate_by = None

    def get_queryset(self) -> QuerySet:
        queryset = Course.objects.prefetch_related(
            "experience", "groups__filia"
        ).distinct()
        sort_option = self.request.GET.get(key="sort", default="name")

        return apply_sorting(queryset, sort_option)


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageCourseAddView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "managers/program_add_course.html"

    def get_success_url(self) -> str:
        course_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Created",
                "object_name": course_name,
                "back_url": reverse("program_manage_courses"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageCourseChangeView(UpdateView):
    form_class = CourseForm
    template_name = "managers/program_change_course.html"
    queryset = Course.objects.all()

    def get_success_url(self) -> str:
        course_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Changed",
                "object_name": course_name,
                "back_url": reverse("program_manage_courses"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageCourseDeleteView(DeleteView):
    template_name = "managers/program_delete_course.html"
    queryset = Course.objects.all()

    def get_success_url(self) -> str:
        course_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Deleted",
                "object_name": course_name,
                "back_url": reverse("program_manage_courses"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ProgramManageGroupsView(FilterView):
    template_name = "managers/program_manage_groups.html"
    context_object_name = "groups"
    filterset_class = GroupFilter
    paginate_by = None

    def get_queryset(self) -> QuerySet:
        queryset = Group.objects.select_related("filia", "course").distinct()
        sort_option = self.request.GET.get(key="sort", default="name")
        return apply_sorting(queryset, sort_option)


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageGroupAddView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "managers/program_add_group.html"

    def get_success_url(self) -> str:
        group_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Created",
                "object_name": group_name,
                "back_url": reverse("program_manage_groups"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ProgramManageGroupChangeView(UpdateView):
    form_class = GroupForm
    template_name = "managers/program_change_group.html"
    queryset = Group.objects.all()

    def get_success_url(self) -> str:
        group_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Changed",
                "object_name": group_name,
                "back_url": reverse("program_manage_groups"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_program_manager)], name="dispatch"
)
class ManageGroupDeleteView(DeleteView):
    template_name = "managers/program_delete_group.html"
    queryset = Group.objects.all()

    def get_success_url(self) -> str:
        group_name = self.object.name
        return reverse(
            "operation_success",
            kwargs={
                "operation_type": "Deleted",
                "object_name": group_name,
                "back_url": reverse("program_manage_groups"),
            },
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_education_manager)],
    name="dispatch",
)
class EducationManageGroupsView(FilterView):
    template_name = "managers/education_manage_groups.html"
    context_object_name = "groups"
    filterset_class = GroupFilter
    paginate_by = None

    def get_queryset(self) -> QuerySet:
        queryset = Group.objects.select_related("filia", "course").distinct()
        sort_option = self.request.GET.get(key="sort", default="name")
        return apply_sorting(queryset, sort_option)


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_education_manager)],
    name="dispatch",
)
class EducationManageGroupDetailsView(TemplateView):
    template_name = "managers/education_manage_group_details.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)

        students = group.students.all().order_by("first_name", "last_name")
        teachers = group.teachers.all().order_by("first_name", "last_name")

        context["group"] = group
        context["students"] = students
        context["teachers"] = teachers
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        group_id = self.kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)

        if "remove_student" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(Student, pk=student_id)
            group.students.remove(student)
            return redirect(
                "operation_success",
                operation_type="Removed",
                object_name=str(student),
                back_url=reverse(
                    "education_manage_group_details", kwargs={"pk": group_id}
                ),
            )

        if "remove_teacher" in request.POST:
            teacher_id = request.POST.get("teacher_id")
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            group.teachers.remove(teacher)
            return redirect(
                "operation_success",
                operation_type="Removed",
                object_name=str(teacher),
                back_url=reverse(
                    "education_manage_group_details", kwargs={"pk": group_id}
                ),
            )

        return redirect("education_manage_group_details", pk=group_id)


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_education_manager)],
    name="dispatch",
)
class EducationManageGroupAddTeachersView(TemplateView):
    template_name = "managers/education_add_teachers_to_group.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, pk=self.kwargs["pk"])
        available_teachers = Teacher.objects.exclude(teacher_groups=group)
        context["group"] = group
        context["available_teachers"] = available_teachers
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        group = get_object_or_404(Group, pk=self.kwargs["pk"])
        teacher_ids = request.POST.getlist("teacher_ids")

        for teacher_id in teacher_ids:
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            group.teachers.add(teacher)

        return redirect(
            "operation_success",
            operation_type="Added",
            object_name=f"{len(teacher_ids)} Teacher(s)",
            back_url=reverse("education_manage_group_details", kwargs={"pk": group.pk}),
        )


@method_decorator(
    [login_required_401, user_passes_test_403(user_is_education_manager)],
    name="dispatch",
)
class EducationManageGroupAddStudentsView(TemplateView):
    template_name = "managers/education_add_students_to_group.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, pk=self.kwargs["pk"])

        available_students = Student.objects.exclude(student_groups=group)
        context["group"] = group
        context["available_students"] = available_students
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        group = get_object_or_404(Group, pk=self.kwargs["pk"])
        student_ids = request.POST.getlist("student_ids")

        for student_id in student_ids:
            student = get_object_or_404(Student, pk=student_id)
            group.students.add(student)

        return redirect(
            "operation_success",
            operation_type="Added",
            object_name=f"{len(student_ids)} Student(s)",
            back_url=reverse("education_manage_group_details", kwargs={"pk": group.pk}),
        )


class FiliaListView(ListView):
    template_name = "unauthorized/filias.html"
    context_object_name = "filias"
    queryset = Filia.objects.all().order_by("name")


class FiliaDetailView(DetailView):
    template_name = "unauthorized/filia_details.html"
    context_object_name = "filia"
    queryset = Filia.objects.prefetch_related("groups__filia")


class CourseListView(FilterView):
    template_name = "unauthorized/courses.html"
    context_object_name = "courses"
    filterset_class = CourseFilter
    paginate_by = None

    def get_queryset(self) -> QuerySet:
        queryset = Course.objects.prefetch_related(
            "experience", "groups__filia"
        ).distinct()
        sort_option = self.request.GET.get(key="sort", default="name")
        return apply_sorting(queryset, sort_option)


class CourseDetailView(DetailView):
    template_name = "unauthorized/course_details.html"
    context_object_name = "course"
    queryset = Course.objects.prefetch_related("experience", "groups__filia")


def contact_success(request: HttpRequest) -> HttpResponse:
    return render(request, "unauthorized/contact_success.html")


@never_cache
def course_quiz(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            request.session["age_group"] = form.cleaned_data["age_group"]
            request.session["experience"] = form.cleaned_data["experience"]
            request.session["learning_goal"] = form.cleaned_data["learning_goal"]

            return redirect("contact_with_quiz")
    else:
        form = SuggestionForm()

    return render(request, "unauthorized/course_quiz.html", {"form": form})


@never_cache
def contact_with_quiz(request: HttpRequest) -> HttpResponse:
    age_group = request.session.get("age_group", "")
    experience = request.session.get("experience", "")
    learning_goal = request.session.get("learning_goal", [])

    if not all([age_group, experience, learning_goal]):
        return redirect("course_quiz")

    suggestion_details = (
        f"Age: {age_group}. Experience: {experience}. Goal: {', '.join(learning_goal)}."
    )
    selected_course = select_course(age_group, experience, learning_goal)

    if selected_course:
        suggested_course_name = selected_course.name
    else:
        suggested_course_name = "No suitable course found."

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.suggested_course = suggested_course_name
            contact_message.suggestion_details = suggestion_details
            contact_message.save()
            return redirect("contact_success")
    else:
        form = ContactForm(
            initial={
                "suggested_course": suggested_course_name,
                "suggestion_details": suggestion_details,
            }
        )

    return render(
        request,
        "unauthorized/contact_with_quiz.html",
        {
            "form": form,
            "suggested_course": suggested_course_name,
            "suggestion_details": suggestion_details,
        },
    )
