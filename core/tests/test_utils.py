import re

import pytz
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from core.utils import *
from core.models import *
from respondent.models import *
from surveyor.models import *


class CoreUtilTestInvalidUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='invalid', email='new@user.com', password='top_secret')

    def test_get_groups(self):
        with self.assertRaises(ValueError):
            get_groups(self.user)

    def test_get_responses(self):
        with self.assertRaises(ValueError):
            get_responses(self.user)


class CoreUtilRespondent(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.task = Task.objects.create(title="", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_2 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_3 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)

    def test_get_responses(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_task(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, task=self.task)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_question(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, question=self.question_1)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_group(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.respondent, group=self.group)
        self.assertEqual(responses.get(), response)

    def test_calculate_score_values(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(calculate_score(values), 5.5)

    def test_calculate_score_values_contains_none(self):
        values = [1, 2, 3, 4, None, 5, 6, 7, 8, 9]
        self.assertEqual(calculate_score(values), 5)

    def test_calculate_score_values_is_empty(self):
        values = []
        self.assertEqual(calculate_score(values), 0)

    def test_get_progress_graphs(self):
        """
        Tests that valid dictionaries containing the graph information are returned
        """
        group_graphs = get_progress_graphs(self.respondent)

        self.assertTrue(group_graphs)
        group_graph = group_graphs[0]

        self.assertEqual(group_graph.keys(), {'id', 'title', 'labels', 'scores'})

        self.assertEqual(group_graph['id'], self.group.id)
        self.assertEqual(group_graph['title'], self.group.name)
        self.assertEqual(group_graph['labels'], [])
        self.assertEqual(group_graph['scores'], [])


class CoreUtilSurveyor(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.groupsurveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_2 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_3 = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)

    def test_get_responses(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_task(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, task=self.task)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_question(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, question=self.question_1)
        self.assertEqual(responses.get(), response)

    def test_get_responses_from_group(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                           date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = get_responses(self.surveyor, group=self.group)
        self.assertEqual(responses.get(), response)

    def test_calculate_score_values(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(calculate_score(values), 5.5)

    def test_calculate_score_values_contains_none(self):
        values = [1, 2, 3, 4, None, 5, 6, 7, 8, 9]
        self.assertEqual(calculate_score(values), 5)

    def test_calculate_score_values_is_empty(self):
        values = []
        self.assertEqual(calculate_score(values), 0)
