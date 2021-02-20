from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from core.views import dashboard, leaderboard
from core.utils import *
from respondent.models import Respondent, GroupRespondent, Response
from surveyor.models import Surveyor, Group, GroupSurveyor, Question

import pytz

class CoreUtilTestInvalidUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='invalid', email='new@user.com', password='top_secret')

    def test_get_groups(self):
        with self.assertRaises(ValueError):
            get_groups(self.user)

    def test_get_graph_labels(self):
        with self.assertRaises(ValueError):
            get_graph_labels(self.user)

    def test_get_responses(self):
        with self.assertRaises(ValueError):
            get_responses(self.user)

class CoreUtilRespondent(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="Shoulder Therapy 1")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
        self.question_2 = Question.objects.create(task=self.task, description="This task was medium", response_type=2)
        self.question_3 = Question.objects.create(task=self.task, description="This task was easy", response_type=3)

    def test_get_responses(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_task(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, task=self.task)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_question(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, question=self.question_1)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_group(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, group=self.group)
        self.assertEqual(responses.get(), response)

    def test_get_graph_labels(self):
        date_time = datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC)
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=date_time)
        labels = get_graph_labels(self.respondent)
        self.assertEqual(labels, [str(date_time.date()), str(date_time.date())])

    def test_get_graph_labels_no_responses(self):
        user = User.objects.create_user(
            username='newuser', email='new@user.com', password='top_secret')
        respondent = Respondent.objects.create(user=user, firstname='New', surname='Testuser')
        labels = get_graph_labels(respondent)
        self.assertFalse(labels)

    def test_get_graph_data(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        labels = get_graph_labels(self.respondent)
        values = get_graph_data(self.respondent, labels)
        self.assertEqual(values, [1, 1])

    def test_get_graph_data_with_empty_labels(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        values = get_graph_data(self.respondent, [])
        self.assertEqual(values, None)

    def test_calculate_score_values(self):
        values = [1,2,3,4,5,6,7,8,9,10]
        self.assertEqual(calculate_score(values), 5.5)

    def test_calculate_score_values_contains_none(self):
        values = [1,2,3,4,None,5,6,7,8,9]
        self.assertEqual(calculate_score(values), 5)

    def test_calculate_score_values_is_empty(self):
        values = []
        self.assertEqual(calculate_score(values), 0)

class CoreUtilSurveyor(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="Shoulder Therapy 1")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.groupsurveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
        self.question_2 = Question.objects.create(task=self.task, description="This task was medium", response_type=2)
        self.question_3 = Question.objects.create(task=self.task, description="This task was easy", response_type=3)

    def test_get_responses(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_task(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, task=self.task)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_question(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, question=self.question_1)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_group(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, group=self.group)
        self.assertEqual(responses.get(), response)

    def test_get_graph_labels(self):
        date_time = datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC)
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=date_time)
        labels = get_graph_labels(self.surveyor)
        self.assertEqual(labels, [str(date_time.date()), str(date_time.date())])

    def test_get_graph_data(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        labels = get_graph_labels(self.surveyor)
        values = get_graph_data(self.respondent, labels)
        self.assertEqual(values, [1, 1])

    def test_get_graph_data_with_empty_labels(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        values = get_graph_data(self.surveyor, [])
        self.assertEqual(values, None)

    def test_calculate_score_values(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(calculate_score(values), 5.5)

    def test_calculate_score_values_contains_none(self):
        values = [1, 2, 3, 4, None, 5, 6, 7, 8, 9]
        self.assertEqual(calculate_score(values), 5)

    def test_calculate_score_values_is_empty(self):
        values = []
        self.assertEqual(calculate_score(values), 0)
