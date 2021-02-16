import datetime

from surveyor.models import Surveyor, Question, Task, Group, GroupSurveyor
from surveyor.views import dashboard, get_tasks_json, get_questions_json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

# TODO

class GetTasksJsonTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')

        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=task, description="This task was difficult", response_type=1)

    def test_response_is_json(self):
        request = self.factory.get('/get_tasks_json')
        request.user = self.user
        response = get_tasks_json(request)
        self.assertTrue(isinstance(JsonResponse, response), response)

    def test_entry_correct_format(self):
        pass

    def test_returns_correct_tasks(self):
        pass


class TaskOverViewTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_task_overview(self):
        pass


class GetQuestionsJsonTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
    
    def test_response_is_json(self):
        request = self.factory.get('/get_questions_json')
        request.user = self.user
        response = get_questions_json(request, self.task.pk)
        self.assertTrue(isinstance(JsonResponse, response), response)

    