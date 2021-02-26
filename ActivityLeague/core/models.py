import uuid

from django.db import models
from surveyor.models import Surveyor


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    admin = models.ForeignKey(Surveyor, on_delete=models.CASCADE)


class SurveyorOrganisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE)