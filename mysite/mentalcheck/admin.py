from django.contrib import admin

from .models import *

admin.site.register(QuestionMC)
admin.site.register(QuestionText)
admin.site.register(Profile)
admin.site.register(additionalNotes)
admin.site.register(Following)
admin.site.register(Support)

# Register your models here.
