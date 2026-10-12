from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):

    technology = models.CharField(max_length=100)

    question = models.TextField()

    topic = models.CharField(max_length=100)

    difficulty = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Interview(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    technology = models.CharField(max_length=100)

    difficulty = models.CharField(max_length=50)

    total_questions = models.PositiveIntegerField()

    score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.technology}"

class InterviewQuestion(models.Model):

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name="interview_questions"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="interview_questions"
    )

    question_order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.interview} - Question {self.question_order}"