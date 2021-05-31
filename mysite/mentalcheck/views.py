from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.timezone import datetime
from django.core.serializers import json


class home(View):
    def get(self, request):
        currUser = request.user
        dateAns = QuestionText.objects.filter(userAnswered = currUser).last().date_answered
        ans_for_today = QuestionText.objects.filter(date_answered = datetime.today()).count()
        qAnswered = False
        if ans_for_today != 0:
            qAnswered = True

        context = {
            "currUser": currUser,
            "ifAnsToday": qAnswered
        }

        return render(request, 'mentalcheck/homepage.html', context)
    def post(self, request):
        if 'profile' in request.POST.keys():
            response = redirect('/mentalcheck/profile/')
        elif 'questions' in request.POST.keys():
            response = redirect('/mentalcheck/questions/')
        elif 'past' in request.POST.keys():
            response = redirect('/mentalcheck/pastAnswers/')
        elif 'following' in request.POST.keys():
            response = redirect('/mentalcheck/following/')
        elif 'logout' in request.POST.keys():
            logout(request)
            return HttpResponse("logged out")

        return response

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
        currProfile = Profile.objects.get(User = currUser)

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
            'allQuestions': QuestionText.objects.all(),
            'currQ': QuestionText.objects.get(idNum = 1)
            # test to see if adding currq as the first will work better
        }
        return render(request, 'mentalcheck/questionspage.html', context)

    # each subsequent question
    def post(self, request):
        # This tests if the form is the log *in* form
        maxId = QuestionText.objects.all().count()
        if 'qFinish' in request.POST.keys():
            response = redirect('/mentalcheck/pastquestions/')
            return response
        elif 'prevId' in request.POST.keys():
            # IF so, try to authenticate
            previousQID = request.POST['prevId']
            prevAns = request.POST[previousQID]
            question = QuestionText.objects.filter(idNum = int(previousQID), userAnswered = request.user).first()
            question.answer = prevAns
            question.date_answered = timezone.now()
            question.save()

        else:
            return HttpResponse("NOOOOOOO")

        context = {
            'currQ': QuestionText.objects.get(idNum = (1 + int(previousQID))),
            'maxId': maxId
        }
        return render(request, 'mentalcheck/questionspage.html', context)

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
                newProfile = Profile.objects.create(User = newUser)
            else:
                return HttpResponse("NOOOOOOO")
        else:
            pass
            # create question objects
        response = redirect('/mentalcheck/questions/')
        return response

class pastAnswer(View):
    def get(self, request):
        pastAnswers = QuestionText.objects.filter(userAnswered = request.user)
        context = {
            'allPastQs': pastAnswers
        }

        return render(request, 'mentalcheck/pastquestionspage.html', context)

class following(View):
    def get(self, request):
        currUser = request.user
        allFollowingF = Following.objects.filter(follower = currUser)
        allFollowersF = Following.objects.filter(followed = currUser)
        allFollowing = []
        allFollowers = []
        for f in allFollowingF:
            allFollowing.append(f.followed)
        for f in allFollowersF:
            allFollowers.append(f.follower)
        allUsers = User.objects.all()
        json_serializer = json.Serializer()
        allUsersJson = json_serializer.serialize(allUsers)

        context = {
            'allFollowing': allFollowing,
            'allFollowers': allFollowers,
            'allUsers': allUsersJson
        }
        return render(request, 'mentalcheck/followingpage.html', context)

    def post(self, request):
        currUser = request.user
        allFollowingF = Following.objects.filter(follower = currUser)
        allFollowersF = Following.objects.filter(followed = currUser)
        allFollowing = []
        allFollowers = []
        for f in allFollowingF:
            allFollowing.append(f.followed)
        for f in allFollowersF:
            allFollowers.append(f.follower)
        allUsers = User.objects.all()
        json_serializer = json.Serializer()
        allUsersJson = json_serializer.serialize(allUsers)

        if 'followUser' in request.POST.keys():
            followedUser = User.objects.get(username = request.POST['userInput'])
            reverseFollowObj = Following.object.filter(follower = followedUser, followed = request.user)
            newFollowObj = Following.objects.create(follower = request.user, followed = followedUser)
            # check if followed back
            if (reverseFollowObj.exists()):
                newFollowObj.followedBack = True
                newFollowObj.save()
                reverseFollowObj.delete()
        else:
            return HttpResponse("NOOOOOOO")

        allFollowObj = Following.object.filter(follower = request.user, followedBack = True)
        allFollowAns = {}
        for f in allFollowObj:
            userName = f.followed.username
            qAns = QuestionText.objects.filter(userAnswered = f.followed, idNum = QuestionText.objects.all().count()).answer
            allFollowAns[userName] = qAns

        context = {
            'allUsers': allUsersJson,
            'allFollowStat': allFollowAns
        }
        return render(request, 'mentalcheck/followingpage.html', context)
