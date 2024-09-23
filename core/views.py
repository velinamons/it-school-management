from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .forms import SuggestionForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def locations(request):
    return render(request, 'locations.html')


def courses(request):
    return render(request, 'courses.html')


def faq(request):
    return render(request, 'faq.html')


def course_quiz_result(request):
    age_group = request.session.get('age_group')
    experience = request.session.get('experience')
    learning_goal = request.session.get('learning_goal')

    del request.session['age_group']
    del request.session['experience']
    del request.session['learning_goal']

    context = {
        'age_group': age_group,
        'experience': experience,
        'learning_goal': learning_goal,
    }
    return render(request, 'course_quiz_result.html', context)


@never_cache
def course_quiz(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            request.session['age_group'] = form.cleaned_data['age_group']
            request.session['experience'] = form.cleaned_data['experience']

            request.session['learning_goal'] = ', '.join(form.cleaned_data['learning_goal'])

            return redirect('course_quiz_result')
    else:
        form = SuggestionForm()

    return render(request, 'course_quiz.html', {'form': form})
