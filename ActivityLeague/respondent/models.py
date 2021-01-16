from django.db import models
from surveyor.models import Group, Question

"""
Django auto generates ID primary keys for each model, 
so these fields have been omitted in the model 
definition here.
"""

class Respondent(models.Model):
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname + " " + self.surname


class GroupRespondent(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    respondent = models.ForeignKey(Respondent, on_delete=models.SET_NULL, null=True)
    value = models.SmallIntegerField()
    date = models.DateField(null=True)
    time = models.TimeField(null=True)