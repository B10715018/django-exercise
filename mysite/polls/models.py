from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        # timedelta measures is publication recently made
        now=timezone.now()
        return now - self.__generateThresholdAcceptedAsRecentTime__()<=self.pub_date<= now

    def __generateThresholdAcceptedAsRecentTime__(self):
        return datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text