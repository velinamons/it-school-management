from django.shortcuts import render


# Create your views here.
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