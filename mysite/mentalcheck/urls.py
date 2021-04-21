from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index.as_view(), name='index'),
    # ex: /polls/5/
    path('profile/', views.profile.as_view(), name='profile'),
    # ex: /polls/5/results/
    path('home/', views.home.as_view(), name='home'),
    # ex: /polls/5/vote/
    path('questions/', views.questions.as_view(), name='questions'),

    path('trends/', views.trends.as_view(), name='trends'),
]
