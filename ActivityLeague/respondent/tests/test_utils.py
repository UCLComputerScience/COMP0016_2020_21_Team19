from django.test import TestCase
from django.contrib.auth.models import User
from respondent import utils
from respondent.models import Respondent, GroupRespondent, Response
from surveyor.models import Task, Group, Question
import datetime
import pytz
import re

class RespondentUtilTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="Shoulder Therapy 1")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
        self.question_2 = Question.objects.create(task=self.task, description="This task was medium", response_type=2)
        self.question_3 = Question.objects.create(task=self.task, description="This task was easy", response_type=3)

    # TODO: This test fails sometimes
    def test_random_hex_colour(self):
        """
        Tests that a valid hex colour is returned
        """
        self.assertTrue(re.match(r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", utils.random_hex_colour()))

    def test_get_chartjs_dict(self):
        """
        Tests that a valid dictionary containing the chart information is returned
        """
        chart_dict = utils.get_chartjs_dict([])
        self.assertEqual(chart_dict.keys(), {'data', 'lineTension', 'backgroundColor', 'borderColor', 'borderWidth', 'pointBackgroundColor'})
    
    def test_get_progress_graphs(self):
        graphs = utils.get_progress_graphs(self.respondent)
        assertEqual(graphs[0].keys(), {'id', 'title', 'labels', 'scores'})