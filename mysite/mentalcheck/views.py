from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils import timezone

class index(View):
    def get(self, request):
        # After we check the forms, set a flag for use in the template.
        if request.user.is_authenticated:
            loggedIn = True
        else:
            loggedIn = False
        context = {
            'user': request.user,
            'loggedIn': loggedIn,
        }
        return render(request, 'mentalcheck/loginpage.html', context)
    def post(self, request):
        if request.POST:
            # This tests if the form is the log *in* form
            if 'inputUsername' in request.POST.keys():
                # IF so, try to authentircate
                user = authenticate(username=request.POST['inputUsername'],
                    password=request.POST['inputPassword'])
                if user is not None:
                    # IF success, then use the login function so the session persists.
                    login(request, user)
                    #return redirect('/mentalcheck/questions/')
                else:
                    pass
                    # Message for failed login.
            # This tests if the form is the log *out* form
            elif 'logout' in request.POST.keys():
                # If so, don't need to check anything else, just kill the session.
                logout(request)

class profile(View):
    def get(self, request):
        # Put info on the page + allow user to edit too
        profiles = Profile.objects.all()
        context = {
            'allProfiles': profiles
        }
        return render(request, 'mentalcheck/profilepage.html', context)

    def post(self, request):
        profiles = Profile.objects.all()
        currUser = request.user
        currProfile = Profile.objects.get(pk = currUser)

        profileAspects = {
            "inputUsername": currUser.username,
            "inputPassword": currUser.password,
            "inputFirstName": currUser.first_name,
            "inputLastName": currUser.last_name,
            "inputAge": currProfile.age,
            "inputMed": currProfile.medicalHistory
        }
        for dataName in profileAspects.keys():
            if dataName in request.POST.keys():
                # IF so, try to authentircate
                textAns = request.POST[dataName]
                if textAns is not None:
                    # IF success, then use the login function so the session persists.
                    profileAspects[dataName] = textAns
                    currUser.save()
                else:
                    pass
                    # Message for failed login.
        context = {
            'allProfiles': profiles
        }
        return render(request, 'mentalcheck/profilepage.html', context)

class questions(View):
    def get(self, request):
        questions = QuestionText.objects.all()
        context = {
            'allQuestions': questions
        }
        return render(request, 'mentalcheck/questionspage.html', context)

    def post(self, request):
        questions = QuestionText.objects.all()
        # This tests if the form is the log *in* form
        for question in questions:
            if str(question.idNum) in request.POST.keys():
                # IF so, try to authentircate
                textAns = request.POST[str(question.idNum)]
                if textAns is not None:
                    # IF success, then use the login function so the session persists.
                    question.answer = textAns
                    question.userAnswered = request.user
                    question.date_answered = timezone.now
                    question.save()
                else:
                    pass
                    # Message for fail

        context = {
            'allQuestions': questions
        }
        return render(request, 'mentalcheck/questionspage.html', context)

class pastAnswer(View):
    def get(self, request):
        pastAnswers = QuestionText.objects.filter(userAnswered = request.user)

        context = {
            'allPastQs': pastAnswers
        }

        return render(request, 'mentalcheck/pastquestionspage.html', context) # How to get just one user's past answers - not everyone's

# Create your views here.
