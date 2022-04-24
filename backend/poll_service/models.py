from django.db import models
from django.contrib.auth.models import User


class Questionnaire(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    users = models.ManyToManyField(
        User,
        blank=True,
        related_name="questionnaires",
        related_query_name="questionnaire",
    )
    is_active = models.BooleanField(default=True)

    def questions_count(self):
        return self.questions.all().count()


class Question(models.Model):
    text = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name="questions",
        related_query_name="question",
        on_delete=models.CASCADE,
    )

    def answers_count(self):
        return self.answers.all().count()

    def votes_count(self):
        return sum(answer.count for answer in self.answers.all())


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )
    count = models.IntegerField(default=0)
