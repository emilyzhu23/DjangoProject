from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('profile/', views.profile, name='profile'),
    # ex: /polls/5/results/
    path('home/', views.home, name='home'),
    # ex: /polls/5/vote/
    path('questions/', views.questions, name='questions'),

    path('trends/', views.trends, name='trends'),
]
