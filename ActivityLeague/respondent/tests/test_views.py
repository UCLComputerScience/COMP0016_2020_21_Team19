from django.test import TestCase, RequestFactory
from respondent import views
from django.urls import reverse
from django.contrib.auth.models import User
from core.views import dashboard, leaderboard
from respondent.models import Respondent, GroupRespondent, Response
from surveyor.models import Surveyor, Task, Group, Question
import datetime
import pytz
import re

class RespondentViewTest(TestCase):
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
    
    # TODO: This test fails sometimes
    def test_random_hex_colour(self):
        """
        Tests that a valid hex colour is returned
        """
        self.assertTrue(re.match(r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", views.random_hex_colour()))
    
    def test_get_chartjs_dict(self):
        """
        Tests that a valid dictionary containing the chart information is returned
        """
        chart_dict = views.get_chartjs_dict([])
        self.assertEqual(chart_dict.keys(), {'data', 'lineTension', 'backgroundColor', 'borderColor', 'borderWidth', 'pointBackgroundColor'})
    
    def test_get_responses(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = views.get_responses(self.user)
        self.assertEqual(responses.get(), response)
    
    def test_get_responses_from_task(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = views.get_responses(self.user, task=self.task)
        self.assertEqual(responses.get(), response)
    
    def test_get_responses_from_question(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = views.get_responses(self.user, question=self.question_1)
        self.assertEqual(responses.get(), response)
    
    def test_get_responses_from_group(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        responses = views.get_responses(self.user, group=self.group)
        self.assertEqual(responses.get(), response)
    
    def test_get_progress_labels(self):
        date_time = datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC)
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=date_time)
        labels = views.get_progress_labels(self.user)
        self.assertEqual(labels, [str(date_time.date()), str(date_time.date())])
    
    def test_get_progress_values(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        labels = views.get_progress_labels(self.user)
        values = views.get_progress_values(self.user, labels)
        self.assertEqual(values, [1, 1])
    
    def test_get_progress_values_with_empty_labels(self):
        response = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, date_time=datetime.datetime(2021, 7, 4, tzinfo=pytz.UTC))
        values = views.get_progress_values(self.user, [])
        self.assertEqual(values, None)

    def test_dashboard(self):
        request = self.factory.get('/dashboard')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_progress(self):
        request = self.factory.get('/progress')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.progress(request)
        self.assertEqual(response.status_code, 200)
    
    def test_get_progress_json(self):
        request = self.factory.get('/get_progress_json')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.get_progress_json(request)
        self.assertEqual(response.status_code, 200)

    def test_response(self):
        request = self.factory.get('/response/')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.response(request, self.task.pk)
        self.assertEqual(response.status_code, 200)

    def test_response_post(self):
        request = self.factory.post('/response', {self.question_1.pk:'agree', self.question_2.pk:'red', self.question_3.pk:'textresponse', 'clicked':''})
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.response(request, self.task.pk)
        self.assertEqual(response.status_code, 302)

    def test_calculate_score_values(self):
        values = [1,2,3,4,5,6,7,8,9,10]
        self.assertEqual(views.calculate_score(values), 5.5)

    def test_calculate_score_values_contains_none(self):
        values = [1,2,3,4,None,5,6,7,8,9]
        self.assertEqual(views.calculate_score(values), 5)

    def test_calculate_score_values_is_empty(self):
        values = []
        self.assertEqual(views.calculate_score(values), 0)