import datetime

from surveyor.models import Surveyor, Question, Task, Group, GroupSurveyor
from surveyor import views
from core.utils import get_tasks
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


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

    def test_response_code_200_if_valid(self):  
        request = self.factory.get('/task/')
        request.user = self.user
        response = views.task_overview(request, self.task.id)
        self.assertEqual(response.status_code, 200)    


class DashboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_dashboard_renders_on_login(self):
        request = self.factory.get('/dashboard')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.dashboard(request)
        self.assertEqual(response.status_code, 200)


class LeaderboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
    
    def test_leaderboard_renders_on_login(self):
        request = self.factory.get('/leaderboard')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.leaderboard(request)
        self.assertEqual(response.status_code, 200)


class NewTaskTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_new_task_renders(self):
        request = self.factory.get('/new_task')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_task(request)
        self.assertEqual(response.status_code, 200)


class GetQuestionsTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)


class NewGroupTestCase(TestCase):
    """
    This is going to be 
    """
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_new_group_renders(self):
        request = self.factory.get('/groups')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_group(request)
        self.assertEqual(response.status_code, 200)


class GroupsTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        group = Group.objects.create(name="Lung Rehabilitation")
        GroupSurveyor.objects.create(surveyor=self.surveyor, group=group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
    
    def test_groups_page_renders_on_login(self):
        request = self.factory.get('/groups')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.groups(request)
        self.assertEqual(response.status_code, 200)


class ManageGroupTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_manage_groups_renders(self):
        request = self.factory.get('/manage_group/')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.manage_group(request)
        self.assertEqual(response.status_code, 200)


class AddUserTestCase(TestCase):
    """
    This returns a JSON response so can be tested more thoroughly
    """
    pass

