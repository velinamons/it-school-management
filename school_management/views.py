from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .forms import SuggestionForm, ContactForm
from .models import Course, Experience, Goal


def filter_courses_by_age(age_group):
    return Course.objects.filter(age_group=age_group)


def filter_courses_by_experience(courses, experience_name):
    return courses.filter(experience__name=experience_name)


def filter_courses_by_goals(courses, learning_goals):
    return courses.filter(goals__name__in=learning_goals).distinct()


def select_course(age_group, experience_name, learning_goals):
    age_filtered_courses = filter_courses_by_age(age_group)
    experience_filtered_courses = filter_courses_by_experience(age_filtered_courses, experience_name)
    goal_matched_courses = filter_courses_by_goals(experience_filtered_courses, learning_goals)

    if goal_matched_courses.exists():
        return goal_matched_courses.first()
    return None


def home(request):
    return render(request, "home.html")


def locations(request):
    return render(request, "locations.html")


def courses(request):
    return render(request, "courses.html")


def contact_success(request):
    return render(request, "contact_success.html")


def login(request):
    return render(request, "authorization/login.html")


def register(request):
    return render(request, "authorization/register.html")


@never_cache
def course_quiz(request):
    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            request.session["age_group"] = form.cleaned_data["age_group"]
            request.session["experience"] = form.cleaned_data["experience"]
            request.session["learning_goal"] = form.cleaned_data["learning_goal"]

            return redirect("contact_with_quiz")
    else:
        form = SuggestionForm()

    return render(request, "course_quiz.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


@never_cache
def contact_with_quiz(request):
    age_group = request.session.get("age_group")
    experience = request.session.get("experience")
    learning_goal = request.session.get("learning_goal")

    if not all([age_group, experience, learning_goal]):
        return redirect('course_quiz')

    suggestion_details = f"Age: {age_group}. Experience: {experience}. Goal: {', '.join(learning_goal)}."
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
        form = ContactForm(initial={
            "suggested_course": suggested_course_name,
            "suggestion_details": suggestion_details
        })

    return render(request, "contact_with_quiz.html", {
        "form": form,
        "suggested_course": suggested_course_name,
        "suggestion_details": suggestion_details
    })
