from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Survey(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.topic + " #" + str(self.id)


class Question(models.Model):
    text = models.CharField(max_length=200, verbose_name="Question Text")
    one_answer_selection = models.BooleanField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name="Answer Text")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Rating(models.Model):
    score = models.IntegerField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return f"Score {self.score} to #{self.survey.id}"


class Results(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    # deleted_q = Question(text="deleted")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # deleted_ans = Answer(text="deleted")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Results"
