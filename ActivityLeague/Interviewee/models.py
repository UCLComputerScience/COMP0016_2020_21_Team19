from django.db import models

"""
Django auto generates ID primary keys for each model, 
so these fields have been omitted in the model 
definition here.
"""

class Interviewee(models.Model):
    pass


class Interviewer(models.Model):
    pass


class Group(models.Model):
    name = models.CharField(max_length=30)


class GroupInterviewer(models.Model):
    interviewer_id = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


class GroupInterviewee(models.Model):
    interviewee_id = models.ForeignKey(Interviewee, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=50)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


class Question(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Response(models.Model):
    value = models.SmallIntegerField()

