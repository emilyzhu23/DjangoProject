from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.timezone import datetime
from django.core.serializers import json
from django.db.models import Q
from django.core.mail import send_mail


# View for home page
class home(View):
    def get(self, request):
        currUser = request.user
        if request.user.is_authenticated:
            print("NOFUCK")
        else:
            print("FUCK")
        print(currUser.username)
        print("FUCK")
        context = {
            "currUser": currUser,
        }
        # pass current user to the template
        return render(request, 'mentalcheck/homepage.html', context)
    def post(self, request):
        # if the user wants to log out
        if 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')
        if 'help' in request.POST.keys():
            sent = send_mail(
                'Hi!',
                "I'm not in a great place mentally at the moment. I would love if you could be there to support me, whether it's listening or just spending time together.",
                request.user.email,
                [Profile.objects.get(User = request.user).emergencyContact],
                fail_silently=False,
            )
            print(sent)

        return response

# View for login page
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
        # if they're signed in v. if they're not
        return render(request, 'mentalcheck/loginpage.html', context)
    def post(self, request):
        if request.POST:
            # if the user is trying to sign in
            if 'newUser' in request.POST.keys():
                # prompt user to make a new account
                print("newUSer")
                response = redirect('/mentalcheck/newuser/')
                return response
            if 'inputUsername' in request.POST.keys():
                user = User.objects.get(username=request.POST['inputUsername'],
                    password=request.POST['inputPassword'])
                if user is not None:
                    # IF success, then use the login function so the session persists.
                    login(request, user)
                    response = redirect('/mentalcheck/home/')
                    return response

            elif 'logout' in request.POST.keys():
                logout(request)
                return render(request, 'mentalcheck/loggedoutpage.html')

# View for editing/looking at own profile
class profile(View):
    def get(self, request):
        # Output all profile info on the page + allow user to edit
        profiles = Profile.objects.all()
        if request.user.is_authenticated:
            currUser = request.user
            currProfile = Profile.objects.get(User = currUser)
        else:
            response = redirect('/mentalcheck/')
            return response

        context = {
            'currProfile': currProfile,
            'currUser': currUser
        }
        return render(request, 'mentalcheck/profilepage.html', context)

    def post(self, request):
        profiles = Profile.objects.all()
        currUser = request.user
        currProfile = Profile.objects.get(User = currUser)

        # check if the user has edited any of the user/profile information
        if "inputUsername" in request.POST.keys():
            currUser.username = request.POST["inputUsername"]
        if "inputFirstName" in request.POST.keys():
            currUser.first_name = request.POST["inputFirstName"]
        if "inputLastName" in request.POST.keys():
            currUser.last_name = request.POST["inputLastName"]
        if "inputAge" in request.POST.keys():
            currProfile.age = request.POST["inputAge"]
        if "inputMed" in request.POST.keys():
            currProfile.medicalHistory = request.POST["inputMed"]
        if "inputSelfEmail" in request.POST.keys():
            currUser.email = request.POST["inputMed"]
        elif 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')
        currUser.save()
        currProfile.save()

        profiles = Profile.objects.all()
        if request.user.is_authenticated:
            currUser = request.user
            currProfile = Profile.objects.get(User = currUser)
        else:
            response = redirect('/mentalcheck/')
            return response

        context = {
            'currProfile': currProfile,
            'currUser': currUser
        }
        return render(request, 'mentalcheck/profilepage.html', context)


# View for questions page - outputs one question at a time, lets user answer
class questions(View):
    # First time loading - load just the first question
    def get(self, request):
        dateAns = Answer.objects.filter(userAnswered = request.user).last().date_answered
        ans_for_today = Answer.objects.filter(date_answered = datetime.today()).count()
        # Check if the questions has already been answered in the past day
        qAnswered = False
        if ans_for_today == 0:
            context = {
                'allQuestions': QuestionText.objects.all(),
                'currQ': QuestionText.objects.get(idNum = 1)
                # test to see if adding currq as the first will work better
            }
            return render(request, 'mentalcheck/questionspage.html', context)
        else:
            return render(request, 'mentalcheck/questionserrorpage.html')

    # each subsequent question
    def post(self, request):
        maxId = QuestionText.objects.all().count() # last question

        if 'prevId' in request.POST.keys(): # move to the next question
            print('prevId')
            previousQID = request.POST['prevId']
            prevAns = request.POST[previousQID]
            answer = Answer.objects.create(userAnswered = request.user, date_answered = timezone.now(), answer = prevAns, questionTextObj = QuestionText.objects.get(id = previousQID))
        if 'qFinish' in request.POST.keys(): # if they're finished with the quiz
            print('qFinish')
            response = redirect('/mentalcheck/home/')
            return response
        elif 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')
        elif 'inputError' in request.POST.keys(): # if the questions have already been answered today
            response = redirect('/mentalcheck/home/')
            return response

        context = {
            'currQ': QuestionText.objects.get(idNum = (1 + int(previousQID))),
            'maxId': maxId
        }
        return render(request, 'mentalcheck/questionspage.html', context)

# View for new user - create new account
class newUser(View):
    allUsernames = []
    def get(self, request):
        return render(request, 'mentalcheck/newuserpage.html')

    def post(self, request):
        allUsers = User.objects.all()
        if "newUsername" in request.POST.keys() and "newPassword" in request.POST.keys() and "newFirstName" in request.POST.keys() and  "newContact" in request.POST.keys() and "newEmail" in request.POST.keys():
            newUserName = request.POST["newUsername"]
            newPassword = request.POST["newPassword"]
            newFirstName = request.POST["newFirstName"]
            newEmail = request.POST["newEmail"]
            newContact = request.POST["newContact"]
            # check to see if the username already exist or not
            if User.objects.filter(username = newUserName).count() == 0:
                newUser = User.objects.create_user(username = newUserName, password = newPassword, first_name = newFirstName, email = newEmail)
                newProfile = Profile.objects.create(User = newUser, emergencyContact = newContact)
            else:
                return render(request, 'mentalcheck/newusererrorpage.html')
        elif 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')

        login(request, newUser)
        response = redirect('/mentalcheck/home/')
        return response

# View for the past answers page - review past answers with their dates
class pastAnswer(View):
    # output all past answers
    def get(self, request):
        pastAnswers = Answer.objects.filter(userAnswered = request.user)
        context = {
            'allPastQs': pastAnswers
        }

        return render(request, 'mentalcheck/pastquestionspage.html', context)
    def post(self, request):
        if 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')

# View for the following page - can find users and follow them, see friends' statuses
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
        # set up for letting the current user to search through all of the other users to follow
        allUsers = User.objects.all()
        json_serializer = json.Serializer()
        allUsersJson = json_serializer.serialize(allUsers)

        allFollowObj = Following.objects.filter(follower = request.user, followedBack = True)
        allFollowAns = {}
        # get statuses of the users who are friends with the current user
        for f in allFollowObj:
            userName = f.followed.username
            maxId = QuestionText.objects.all().count()
            questionTextObjAns = QuestionText.objects.get(idNum = maxId)
            print(questionTextObjAns)
            qAns = Answer.objects.filter(userAnswered = f.followed, questionTextObj = questionTextObjAns).first()
            print(qAns)
            allFollowAns[userName] = qAns.answer


        context = {
            'allUsers': allUsersJson,
            'allFollowAns': allFollowAns
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

        # if the current user follows another user
        if 'followUser' in request.POST.keys():
            followedUser = User.objects.get(username = request.POST['userInput'])
            reverseFollowObj = Following.object.filter(follower = followedUser, followed = request.user)
            newFollowObj = Following.objects.create(follower = request.user, followed = followedUser)
            # check if the users follow each other back
            if (reverseFollowObj.exists()):
                newFollowObj.followedBack = True
                newFollowObj.save()
                reverseFollowObj.followedBack = True
                reverseFollowObj.save()
        elif 'logout' in request.POST.keys():
            logout(request)
            return render(request, 'mentalcheck/loggedoutpage.html')
        else:
            return render(request, 'mentalcheck/followingerrorpage.html')

        allFollowObj = Following.object.filter(follower = request.user, followedBack = True)
        allFollowAns = {}
        # get statuses of the users who are friends with the current user
        for f in allFollowObj:
            userName = f.followed.username
            qAns = Answer.objects.filter(userAnswered = f.followed, questionTextObj = QuestionText.objects.filter(idNum = QuestionText.objects.all().count())).answer
            allFollowAns[userName] = qAns

        context = {
            'allUsers': allUsersJson,
            'allFollowStat': allFollowAns
        }
        return render(request, 'mentalcheck/followingpage.html', context)
