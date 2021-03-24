from django.shortcuts import render, loader
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    if request.POST:
        # This tests if the form is the log *in* form
        if 'inputUsername' in request.POST.keys():
            # IF so, try to authentircate
            user = authenticate(username=request.POST['inputUsername'],
                password=request.POST['inputPassword'])
            if user is not None:
                # IF success, then use the login function so the session persists.
                login(request, user)
            else:
                pass
                # Message for failed login.
        # This tests if the form is the log *out* form
        elif 'logout' in request.POST.keys():
            # If so, don't need to check anything else, just kill the session.
            logout(request)
    # After we check the forms, set a flag for use in the template.
    if request.user.is_authenticated:
        loggedIn = True
    else:
        loggedIn = False
    template = loader.get_template('mentalcheck/loginpage.html')
    context = {
        'user': request.user,
        'loggedIn': loggedIn,
    }
    return render(request, 'mentalcheck/loginpage.html', context)

def profile(request):
    # Put info on the page + allow user to edit too
    template = loader.get_template('mentalcheck/profilepage.html')
    context = {
        'profile': Profile,
        'user': user,
    }
    return render(request, 'mentalcheck/profilepage.html', context)

def home(request):
    return HttpResponse("HOME")

def questions(request):
    return HttpResponse("QUESTIONS")

def trends(request):
    return HttpResponse("TRENDS")

# Create your views here.
