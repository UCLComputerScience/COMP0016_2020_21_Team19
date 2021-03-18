import datetime

import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from surveyor import views
from core.models import *
from respondent.models import *
from surveyor.models import *

"""
Testing invalid GET requests is unnecessary - it is the same as testing Django's
internal get_object_or_404 which is assumed to work.
"""

def _setUp(testcase):
    testcase.factory = RequestFactory()
    testcase.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
    testcase.surveyor = Surveyor.objects.create(user=testcase.user, firstname='Jane', surname='White')
    testcase.group = Group.objects.create(name="Lung Rehabilitation")
    testcase.group_surveyor = GroupSurveyor.objects.create(surveyor=testcase.surveyor, group=testcase.group)
    testcase.task = Task.objects.create(title="Perform 20 Press-Ups", group=testcase.group,
                                    due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                    due_time=datetime.time(10, 0))

    testcase.question = Question.objects.create(task=testcase.task, description="This task was difficult", response_type=Question.ResponseType.LIKERT_ASC)

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
        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=Question.ResponseType.LIKERT_ASC)

    def test_response_code_200_if_valid(self):
        """
        Accessing /task/ should give status code of 200. Accessing /task/a where a is an invalid
        UUID should not give you a status code of 404, though we know this behaviour is already defined
        given the internal dependency on the django-core get_object_or_404 method which has already
        been extensively tested.
        """
        request = self.factory.get(reverse('task_overview', args=[self.task.id]))
        request.user = self.user
        response = views.task_overview(request, self.task.id)
        self.assertEqual(response.status_code, 200)


class DashboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        _setUp(self)

    def test_response_code_200_if_valid_path(self):
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.dashboard(request)
        self.assertEqual(response.status_code, 200)


class LeaderboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        _setUp(self)

    def test_response_code_200_if_valid_path(self):
        request = self.factory.get(reverse('leaderboard'))
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
        request = self.factory.get(reverse('new-task'))
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_task(request)
        self.assertEqual(response.status_code, 200)

class GroupsTestCase(TestCase):

    @classmethod
    def setUp(self):
        _setUp(self)

    def test_response_code_200_if_valid_login(self):
        request = self.factory.get(reverse('groups'))
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
        request = self.factory.get(reverse('manage-group', args=[self.group.id]))
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.manage_group(request, self.group.id)
        self.assertEqual(response.status_code, 200)

    def test_manage_group_post(self):
        self.client.login(username='jane', password='activityleague')
        payload = {'respondent': self.respondent.id}
        request = self.client.post(reverse('manage-group', args=[self.group.id]), payload)
        group_respondent = GroupRespondent.objects.get(respondent=self.respondent)
        self.assertEqual(group_respondent.group, self.group)


class HistoryTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        
    def test_response_code_200_if_valid(self):
        """
        A valid GET request to `/history` should yield a response code of 200.
        """
        self.client.login(username='jane', password='activityleague')
        request = self.factory.get(reverse('history'))
        request.user = self.user
        response = views.history(request)
        self.assertEqual(response.status_code, 200)
    

class OrganisationTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.organisation = Organisation.objects.create(name="")
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White', organisation=self.organisation)
    
    def test_response_code_200_if_get(self):
        self.client.login(username='jane', password='activityleague')
        request = self.factory.get(reverse('organisation'))
        request.user = self.user
        response = views.organisation(request)
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_302_if_post(self):
        self.client.login(username='jane', password='activityleague')
        request = self.factory.post(reverse('organisation'))
        request.user = self.user
        response = views.organisation(request)
        self.assertEqual(response.status_code, 302)


class UsersTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.organisation = Organisation.objects.create(name="")
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White', organisation=self.organisation)
    
    def test_response_code_200_if_get(self):
        request = self.factory.get(reverse('users'))
        request.user = self.user
        response = views.users(request)
        self.assertEqual(response.status_code, 200)
    

class UserProgressTestCase(TestCase):

    def setUp(self):
        _setUp(self)
        self.question_1 = Question.objects.create(task=self.task, description='Text Neutral Question', response_type=Question.ResponseType.TEXT_NEUTRAL)
        self.question_2 = Question.objects.create(task=self.task, description='Text Negative Question', response_type=Question.ResponseType.TEXT_NEGATIVE)
        self.question_3 = Question.objects.create(task=self.task, description='Text Positive Question', response_type=Question.ResponseType.TEXT_POSITIVE)
        self.respondent_user = User.objects.create_user(username='Emma', email='emma@email.com', password='activityleague')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='Emma', surname='Green')
        self.group_respondent = GroupRespondent.objects.create(group=self.group, respondent=self.respondent)
        self.response_1 = Response.objects.create(question=self.question_1, respondent=self.respondent, value=None, text="Test Neutral", text_positive=None, date_time=timezone.now())
        self.response_2 = Response.objects.create(question=self.question_2, respondent=self.respondent, value=None, text="Test Negative", text_positive=False, date_time=timezone.now())
        self.response_3 = Response.objects.create(question=self.question_3, respondent=self.respondent, value=None, text="Test Positive", text_positive=True, date_time=timezone.now())

    def test_response_code_200_if_get(self):
        request = self.factory.get(reverse('user_progress', args=[self.respondent.id]))
        request.user = self.user
        response = views.user_progress(request, self.respondent.id)
        self.assertEqual(response.status_code, 200)


class UserResponseTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.surveyor_user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.respondent_user = User.objects.create_user(username='john', email='john@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.surveyor_user, firstname='', surname='')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='', surname='')
        self.group = Group.objects.create(name="")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.group_respondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.task = Task.objects.create(title="", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))
        self.question = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.response = Response.objects.create(question=self.question, respondent=self.respondent, value=1, date_time=timezone.now())
    
    def test_response_code_200_if_valid(self):
        request = self.factory.get(reverse('user_response', args=[self.respondent.id, self.task.id]))
        request.user = self.surveyor_user
        response = views.user_response(request, self.respondent.id, self.task.id)
        self.assertEqual(response.status_code, 200)
