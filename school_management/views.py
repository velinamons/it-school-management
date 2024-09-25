from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .forms import SuggestionForm, ContactForm
from .course_suggestion_logic import select_course, courses as courses_tuple


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def locations(request):
    return render(request, "locations.html")


def courses(request):
    return render(request, "courses.html")


def faq(request):
    return render(request, "faq.html")


def contact_success(request):
    return render(request, "contact_success.html")


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

    suggested_course = select_course(courses_tuple, age_group, experience, learning_goal)
    suggestion_details = f"Age: {age_group}. Experience: {experience}. Goal: {', '.join(learning_goal)}."

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.suggested_course = suggested_course
            contact_message.suggestion_details = suggestion_details
            contact_message.save()
            return redirect("contact_success")
    else:
        form = ContactForm(initial={
            "suggested_course": suggested_course,
            "suggestion_details": suggestion_details
        })

    return render(request, "contact_with_quiz.html", {
        "form": form,
        "suggested_course": suggested_course,
        "suggestion_details": suggestion_details
    })
