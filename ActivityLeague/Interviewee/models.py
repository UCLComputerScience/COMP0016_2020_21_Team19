from Interviewer.models import Group, Question
from django.db import models

"""
Django auto generates ID primary keys for each model, 
so these fields have been omitted in the model 
definition here.
"""

class Interviewee(models.Model):
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname + " " + self.surname


# class GroupInterviewee(models.Model):
#     interviewee_id = models.ForeignKey(Interviewee, on_delete=models.CASCADE)
#     group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


class Response(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    interviewee_id = models.ForeignKey(Interviewee, on_delete=models.SET_NULL, null=True)
    value = models.SmallIntegerField()

