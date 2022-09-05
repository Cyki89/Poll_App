from django.contrib import admin

from .models import Questionnaire, Question, Answer

admin.site.register((Questionnaire, Question, Answer))
