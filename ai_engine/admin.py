from django.contrib import admin

from .models import Question, Interview, InterviewQuestion


admin.site.register(Question)
admin.site.register(Interview)
admin.site.register(InterviewQuestion)