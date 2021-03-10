from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
class QuestionMC(models.Model):
    answerChoices = (
        ('a', 'x'),
        ('b', 'y'),
        ('c', 'z'),
    )
    answer = models.CharField(max_length=1, choices=answerChoices)
    date = models.DateField()
    user = models.ForeignKey(User)
class QuestionText(models.Model):
    date = models.DateField()
    answer = models.CharField(max_length=60)
    user = models.ForeignKey(User)
class Support(models.Model):
    ifSupportNeeded = models.CharField(max_length=30)
    user = models.ForeignKey(User)
# Create your models here.
