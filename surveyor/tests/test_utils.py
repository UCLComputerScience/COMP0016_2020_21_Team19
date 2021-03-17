import datetime

import pytz
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from surveyor import utils
from core.models import *
from respondent.models import *
from surveyor.models import *


class GetQuestionsTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.surveyor_user = User.objects.create_user(username='jane', email='jane@email.com',
                                                      password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.surveyor_user, firstname='Jane', surname='White')
        self.respondent_user = User.objects.create_user(username='Emma', email='emma@email.com',
                                                        password='activityleague')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='Emma', surname='Green')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)

        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC),
                                        due_time=datetime.time(10, 0))

        self.question_1 = Question.objects.create(task=self.task, description="Walk for 2 miles", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_2 = Question.objects.create(task=self.task, description="Socialise with 2 people today",
                                                  response_type=Question.ResponseType.TRAFFIC_LIGHT)
        self.question_3 = Question.objects.create(task=self.task,
                                                  description="Spend less than 1h per day on your phone",
                                                  response_type=Question.ResponseType.TEXT_NEUTRAL)

        self.response_1 = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1,
                                                  text=None,
                                                  date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC),
                                                  link_clicked=True)
        self.response_2 = Response.objects.create(question=self.question_2, respondent=self.respondent, value=1,
                                                  text=None,
                                                  date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC),
                                                  link_clicked=True)
        self.response_3 = Response.objects.create(question=self.question_3, respondent=self.respondent, value=None,
                                                  text='Hard',
                                                  date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC),
                                                  link_clicked=True)

    def test_data_formatted_appropriately(self):
        """
        Each dictionary in the list data should contain keys: id, link, type, description, link_clicks, chart_labels,
        chart_data, word_cloud.
        """
        data = utils.get_task_summary(self.task.id)
        self.assertTrue(data)
        entry = data[0]
        self.assertEqual(entry.keys(), {'question', 'link_clicks', 'chart_labels', 'chart_data'})

    def test_chart_likert_labels_correct(self):
        """
        Questions with response_type = 1 (likert questions) should have labels: 'Strongly Disagree', 'Disagree', 'Neutral',
        'Agree', 'Strongly Agree'.
        """
        data = utils.get_task_summary(self.task.id)
        likert_entry = None
        for entry in data:
            if entry['question'].is_likert:
                likert_entry = entry
                break
        self.assertEqual(likert_entry['chart_labels'],
                         ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])

    def test_chart_traffic_labels_correct(self):
        """
        Questions with response_type = 2 (traffic light questions) should have labels: 'Red', 'Yellow', 'Green'.
        """
        data = utils.get_task_summary(self.task.id)
        traffic_entry = None
        for entry in data:
            if entry['question'].is_traffic_light:
                traffic_entry = entry
                break
        self.assertEqual(traffic_entry['chart_labels'], ['Red', 'Yellow', 'Green'])

    def test_word_cloud_url_correct(self):
        """
        If a question contains a text-based response, we should get a link to a generated word cloud image
        of the form 'data:image/png;base64' + string.
        """
        data = utils.get_task_summary(self.task.id)
        text_entry = None
        for entry in data:
            if entry['question'].is_text:
                text_entry = entry
                break
        self.assertTrue(text_entry['chart_data'].startswith('data:image/png;base64'))

    def test_link_clicks_correct(self):
        """
        Tests whether the number of link clicks returned is the same as the number of link clicks recorded
        per question.
        """
        data = utils.get_task_summary(self.task.id)
        clicks = []
        for i in range(0, 3):
            clicks.append(1 if data[i]['link_clicks'] else 0)
        self.assertEqual(clicks, [1, 1, 1])

    def test_question_descriptions_correct(self):
        """
        Tests whether the descriptions to each of the questions returned are correct: we do not return
        any descriptions of questions that are not part of the task and do not neglect any descriptions
        that are part of the task.
        """
        data = utils.get_task_summary(self.task.id)
        descriptions = {entry['question'].description for entry in data}
        self.assertEqual(descriptions, {"Walk for 2 miles", "Socialise with 2 people today",
                                        "Spend less than 1h per day on your phone"})
