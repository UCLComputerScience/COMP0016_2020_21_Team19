import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import Group, Question


class Respondent(models.Model):
    """
    Model representing a ``Respondent``.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname + " " + self.surname


class GroupRespondent(models.Model):
    """
    Model representing a ``Respondent`` in a ``Group``.
    For each ``Group`` that a ``Respondent`` is in, a corresponding ``GroupRespondent`` is created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Response(models.Model):
    """
    Model representing a ``Response``.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    respondent = models.ForeignKey(Respondent, on_delete=models.SET_NULL, null=True)
    value = models.FloatField(null=True)
    text = models.CharField(max_length=30, null=True)
    text_positive = models.BooleanField(null=True, default=None)
    date_time = models.DateTimeField()
    link_clicked = models.BooleanField(default=False)
