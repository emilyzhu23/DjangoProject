from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index.as_view(), name='index'),

    path('home/', views.home.as_view(), name='home'),
    # ex: /polls/5/
    path('profile/', views.profile.as_view(), name='profile'),

    path('newuser/', views.newUser.as_view(), name='newuser'),

    path('questions/', views.questions.as_view(), name='questions'),

    path('pastAnswers/', views.pastAnswer.as_view(), name='pastAnswers'),

    path('following/', views.following.as_view(), name='following')
]
