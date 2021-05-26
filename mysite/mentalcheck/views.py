from django.shortcuts import render, redirect, get_object_or_404
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
                    response = redirect('/mentalcheck/questions/')
                    return response
                else:
                    pass
                    # Message for failed login.
            # This tests if the form is the log *out* form
            elif 'logout' in request.POST.keys():
                # If so, don't need to check anything else, just kill the session.
                logout(request)
            elif 'newUser' in request.POST.keys():
                response = redirect('/mentalcheck/newuser/')
                return response

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
    # First time loading
    def get(self, request):
        context = {
            'allQuestions': QuestionText.objects.all()
        }
        return render(request, 'mentalcheck/questionspage.html', context)

    # each subsequent question
    def post(self, request):
        questions = QuestionText.objects.all()
        # This tests if the form is the log *in* form
        for question in questions:
            if str(question.idNum) in request.POST.keys():
                # IF so, try to authenticate
                textAns = request.POST[str(question.idNum)]
                if textAns is not None:
                    # IF success, then use the login function so the session persists.
                    question.answer = textAns
                    question.userAnswered = request.user
                    question.date_answered = timezone.now
                    question.save()
                else:
                    pass
            # create page with one question at a time
            context = {
                'currQ': question
            }
            return render(request, 'mentalcheck/questionspage.html', context)
            # reload page - how to get data from one session to the next???
            response = redirect('/mentalcheck/questions/')
            return response

class newUser(View):
    allUsernames = []
    def get(self, request):
        return render(request, 'mentalcheck/newuserpage.html')

    def post(self, request):
        allUsers = User.objects.all()
        if "newUsername" in request.POST.keys() and "newPassword" in request.POST.keys() and "newFirstName" in request.POST.keys():
            newUserName = request.POST["newUsername"]
            newPassword = request.POST["newPassword"]
            newFirstName = request.POST["newFirstName"]
            if User.objects.filter(username = newUserName).count() == 0:
                newUser = User.objects.create_user(username = newUserName, password = newPassword, first_name = newFirstName)
            else:
                return HttpResponse("NOOOOOOO")
        else:
            pass

        response = redirect('/mentalcheck/questions/')
        return response

class pastAnswer(View):
    def get(self, request):
        pastAnswers = QuestionText.objects.filter(pk = request.user)
        context = {
            'allPastQs': pastAnswers
        }

        return render(request, 'mentalcheck/pastquestionspage.html', context)

class following(View):
    def get(self, request):
        allFollowing = request.user.followed.all()
        allFollowers = request.user.follower.all()
        context = {
            'allFollowing': allFollowing,
            'allFollowers': allFollowers
        }
        return render(request, 'mentalcheck/followingpage.html', context)

    def post(self, request):
        if 'searchedUser' in request.POST.keys():
            query = self.request.POST.get('searchedUser')
            if query != None:
                searchUser = User.objects.get(username__icontains=query)
                Following.objects.create(follower = request.user, following = searchUser)
            else:
                return HttpResponse("NOOOOOOO")
                # how to create new following models ig?
        else:
            return HttpResponse("user dne")
            
        allFollowing = request.user.followed.all()
        allFollowers = request.user.follower.all()
        context = {
            'allFollowing': allFollowing,
            'allFollowers': allFollowers
        }
        return render(request, 'mentalcheck/followingpage.html', context)
