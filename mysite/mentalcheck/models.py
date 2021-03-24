from django.db import models
from django.contrib.auth.models import User

class QuestionMC(models.Model):
    answerChoices = (
        ('a', 'Sad'),
        ('b', 'Stressed'),
        ('c', 'Happy'),
        ('d', 'Angry'),
        ('e', 'Nervous'),
        ('f', 'Tired'),
    )
    answer = models.CharField(max_length=1, choices=answerChoices)
    date = models.DateField('date answered')
    userAnswered = models.ForeignKey(User, on_delete = models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    age = models.IntegerField()
    medicalHistory = models.TextField(default="", blank=True)
    emergencyContact = models.CharField(max_length = 10, default = "")

class QuestionText(models.Model):
    date = models.DateField()
    answer = models.CharField(max_length=60)
    userAnswered = models.ForeignKey(User, on_delete = models.CASCADE)

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

class additionalNotes(models.Model):
    notes = models.TextField(default="", blank=True)
    userAnswered = models.ForeignKey(User, on_delete = models.CASCADE)

class Support(models.Model):
    ifSupportNeeded = models.CharField(max_length=30)

# https://docs.djangoproject.com/en/3.1/intro/tutorial02/
