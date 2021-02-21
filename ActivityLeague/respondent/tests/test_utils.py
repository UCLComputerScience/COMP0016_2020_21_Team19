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
        hex_colour = utils.random_hex_colour()
        self.assertTrue(re.match(r"^#([a-fA-F0-9]{6})$", hex_colour))

    def test_get_chartjs_dict(self):
        """
        Tests that a valid dictionary containing the chart information is returned
        """
        chart_dict = utils.get_chartjs_dict([])
        self.assertEqual(chart_dict.keys(), {'data', 'lineTension', 'backgroundColor', 'borderColor', 'borderWidth', 'pointBackgroundColor'})
    
    def test_get_progress_graphs(self):
        """
        Tests that valid dictionaries containing the graph information are returned
        """
        graphs = utils.get_progress_graphs(self.respondent)
        self.assertTrue(len(graphs) == 2)
        overall_graph = graphs[0]
        group_graph = graphs[1]
        self.assertEqual(overall_graph.keys(), {'id', 'title', 'labels', 'scores'})

        self.assertEqual(overall_graph['id'], 'overall')
        self.assertEqual(overall_graph['title'], 'Overall')
        self.assertEqual(overall_graph['labels'], [])
        self.assertTrue(overall_graph['scores'])
        self.assertEqual(overall_graph['scores'][0].keys(), {'data', 'lineTension', 'backgroundColor', 'borderColor', 'borderWidth', 'pointBackgroundColor'})
        self.assertEqual(overall_graph['scores'][0]['data'], [])

        self.assertEqual(group_graph['id'], self.group.id)
        self.assertEqual(group_graph['title'], self.group.name)
        self.assertEqual(group_graph['labels'], [])
        self.assertTrue(group_graph['scores'])
        self.assertEqual(group_graph['scores'][0].keys(), {'data', 'lineTension', 'backgroundColor', 'borderColor', 'borderWidth', 'pointBackgroundColor'})
        self.assertEqual(group_graph['scores'][0]['data'], [])