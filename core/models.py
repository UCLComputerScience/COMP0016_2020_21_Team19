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

    @property
    def is_ascending(self):
        return self.response_type in [
            Question.ResponseType.LIKERT_ASC,
            Question.ResponseType.TRAFFIC_LIGHT,
            Question.ResponseType.NUMERICAL_ASC
        ]
    
    @property
    def is_descending(self):
        return self.response_type in [
            Question.ResponseType.LIKERT_DESC,
            Question.ResponseType.NUMERICAL_DESC
        ]

    @property
    def is_likert(self):
        return self.response_type in [
            Question.ResponseType.LIKERT_ASC,
            Question.ResponseType.LIKERT_DESC
        ]
    
    @property
    def is_text(self):
        return self.response_type in [
            Question.ResponseType.TEXT_NEUTRAL,
            Question.ResponseType.TEXT_POSITIVE,
            Question.ResponseType.TEXT_NEGATIVE
        ]
    
    @property
    def is_numerical(self):
        return self.response_type in [
            Question.ResponseType.NUMERICAL_ASC,
            Question.ResponseType.NUMERICAL_DESC
        ]
    
    @property
    def is_traffic_light(self):
        return self.response_type == Question.ResponseType.TRAFFIC_LIGHT

    @property
    def is_text_neutral(self):
        return self.response_type == Question.ResponseType.TEXT_NEUTRAL

    @property
    def is_text_negative(self):
        return self.response_type == Question.ResponseType.TEXT_NEGATIVE

    @property
    def is_text_positive(self):
        return self.response_type == Question.ResponseType.TEXT_POSITIVE

    def mark_as_complete(self):
        self.completed = True
        self.save()

    def mark_as_incomplete(self):
        self.completed = False
        self.save()

    def get_labels(self):
        if self.is_likert:
            return ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
        elif self.is_traffic_light:
            return ['Red', 'Yellow', 'Green']
        elif self.is_numerical:
            return ['1', '2', '3', '4', '5']
        else:
            return None
    
    @property
    def traffic_light_sad_value(self):
        return 5 / 3
    
    @property
    def traffic_light_neutral_value(self):
        return (5 / 3) * 2
    
    @property
    def traffic_light_happy_value(self):
        return 5
    
    def get_values_list(self):
        if self.is_likert or self.is_numerical:
            return [1, 2, 3, 4, 5]
        elif self.is_traffic_light:
            return [self.traffic_light_sad_value, self.traffic_light_neutral_value, self.traffic_light_happy_value]
        else:
            return None