from django.shortcuts import render
from django.http import HttpResponse

def shows(request):
    return render(request, 'plays/shows.html')

def about(request):
    return render(request, 'plays/about.html')

def feedback(request):
    return render(request, 'plays/feedback.html')

def maps(request):
    return render(request, 'plays/maps.html')

def login(request):
    return render(request, 'plays/login.html')

def signup(request):
    return render(request, 'plays/signup.html')

def profile(request):
    return