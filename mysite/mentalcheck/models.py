from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    questions = models.ManyToManyField(QuestionMC)
class QuestionMC(models.Model):
    answerChoices = (
        ('a', 'x'),
        ('b', 'y'),
        ('c', 'z'),
    )
    answer = models.CharField(max_length=1, choices=answerChoices)
    date = models.DateField()
class QuestionText(models.Model):
    date = models.DateField()
    answer = models.CharField(max_length=60)
class Support(models.Model):
    ifSupportNeeded = models.CharField(max_length=30)

# Create your models here.
