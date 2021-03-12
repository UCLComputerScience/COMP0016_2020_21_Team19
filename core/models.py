import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    due_date = models.DateField()
    due_time = models.TimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    class ResponseType(models.IntegerChoices):
        LIKERT_ASC = 1, _('Likert Scale (Agree is better)')
        LIKERT_DESC = 8, _('Likert Scale (Disagree is better)')
        TRAFFIC_LIGHT = 2, _('Traffic Light')
        NUMERICAL_ASC = 3, _('1-5 (Higher is better)')
        NUMERICAL_DESC = 7, _('1-5 (Lower is better)')
        TEXT_NEUTRAL = 4, _('Text (Neutral)')
        TEXT_POSITIVE = 5, _('Text (Positive)')
        TEXT_NEGATIVE = 6, _('Text (Negative)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
    link = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=False)
    response_type = models.IntegerField(choices=ResponseType.choices)
