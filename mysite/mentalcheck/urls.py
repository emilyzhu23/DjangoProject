from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index.as_view(), name='index'),
    # ex: /polls/5/
    path('profile/', views.profile.as_view(), name='profile'),

    path('questions/', views.questions.as_view(), name='questions'),

    path('pastAnswers/', views.pastAnswer.as_view(), name='trends'),
]
