from django.db import models

"""
Django auto generates ID primary keys for each model, 
so these fields have been omitted in the model 
definition here.
"""

class Surveyor(models.Model):
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname + " " + self.surname


class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class GroupSurveyor(models.Model):
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    response_type = models.SmallIntegerField()