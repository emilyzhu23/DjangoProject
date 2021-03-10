from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return HttpResponse("LOGIN")

def profile(request):
    return HttpResponse("PROFILE")

def home(request):
    return HttpResponse("HOME")

def questions(request):
    return HttpResponse("QUESTIONS")

def trends(request):
    return HttpResponse("TRENDS")

# Create your views here.
