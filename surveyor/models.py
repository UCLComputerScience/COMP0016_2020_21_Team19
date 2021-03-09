import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import Group


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    admin = models.OneToOneField('Surveyor', related_name='+', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Surveyor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.firstname + " " + self.surname


class GroupSurveyor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class TaskTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class QuestionTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    link = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=False)
    response_type = models.SmallIntegerField()
