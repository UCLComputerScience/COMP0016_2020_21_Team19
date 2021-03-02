import datetime

import pytz
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from respondent.models import Respondent, GroupRespondent
from surveyor import views
from surveyor.models import Surveyor, Question, Task, Group, GroupSurveyor


class TaskOverViewTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                        due_time=datetime.time(10, 0))
        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_response_code_200_if_valid(self):
        """
        Accessing /task/ should give status code of 200. Accessing /task/a where a is an invalid
        UUID should not give you a status code of 404, though we know this behaviour is already defined
        given the internal dependency on the django-core get_object_or_404 method which has already
        been extensively tested.
        """
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
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                        due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_response_code_200_if_valid_path(self):
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
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                        due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_response_code_200_if_valid_path(self):
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

    def test_response_code_200_if_valid_path(self):
        request = self.factory.get('/new-task')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_task(request)
        self.assertEqual(response.status_code, 200)


class NewGroupTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')

    def test_response_code_200_if_valid_path(self):
        self.client.login(username='jane', password='activityleague')
        request = self.factory.get('/new-group')
        request.user = self.user
        response = views.new_group(request)
        self.assertEqual(response.status_code, 200)

    def test_new_group_post(self):
        self.client.login(username='jane', password='activityleague')
        request = self.client.post('/new-group', {'name': 'Shoulder Therapy 1'})
        self.assertTrue(Group.objects.filter(name="Shoulder Therapy 1").exists())
        group = Group.objects.get(name="Shoulder Therapy 1")
        self.assertTrue(GroupSurveyor.objects.filter(surveyor=self.surveyor, group=group).exists())


class GroupsTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                        due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_response_code_200_if_valid_login(self):
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
        self.respondent_user = User.objects.create_user(username='Emma', email='emma@email.com',
                                                        password='activityleague')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='Emma', surname='Green')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)

    def test_response_code_200_if_valid(self):
        request = self.factory.get('/manage-group/')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.manage_group(request, self.group.id)
        self.assertEqual(response.status_code, 200)

    def test_manage_group_post(self):
        self.client.login(username='jane', password='activityleague')
        request = self.client.post('/manage-group/' + str(self.group.id), {'respondent': self.respondent.id})
        group_respondent = GroupRespondent.objects.get(respondent=self.respondent)
        self.assertEqual(group_respondent.group, self.group)
