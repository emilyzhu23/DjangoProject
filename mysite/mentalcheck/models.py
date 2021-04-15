from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True,
    )
    age = models.IntegerField()
    medicalHistory = models.TextField(default="", blank=True)
    emergencyContact = models.CharField(max_length = 10, default = "")

class QuestionText(models.Model):
    date = models.DateField()
    answer = models.CharField(max_length=60)
    userAnswered = models.ForeignKey(User, on_delete = models.CASCADE, default = "")

class Following(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True,
        related_name = 'follower'
    )

    followed = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True,
        related_name = 'followed'
    )

    questionsShared = models.BooleanField(default=False)

# https://docs.djangoproject.com/en/3.1/intro/tutorial02/
