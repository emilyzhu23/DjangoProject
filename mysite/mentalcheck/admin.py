from django.contrib import admin

from .models import *

admin.site.register(QuestionText)
admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Answer)

# Register your models here.
