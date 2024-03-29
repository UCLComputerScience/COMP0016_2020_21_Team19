import datetime

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from core.views import dashboard, leaderboard
from respondent import views
from core.models import *
from respondent.models import *
from surveyor.models import *

"""
Testing invalid GET requests is unnecessary - it is the same as testing Django's
internal get_object_or_404 which is assumed to work.
"""

class RespondentViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')
        self.respondent = Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        self.group = Group.objects.create(name="Shoulder Therapy 1")
        self.grouprespondent = GroupRespondent.objects.create(respondent=self.respondent, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group,
                                        due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.question_1 = Question.objects.create(task=self.task, description="This task was difficult", response_type=Question.ResponseType.LIKERT_ASC)
        self.question_2 = Question.objects.create(task=self.task, description="This task was medium", response_type=Question.ResponseType.TRAFFIC_LIGHT)
        self.question_3 = Question.objects.create(task=self.task, description="This task was easy", response_type=Question.ResponseType.TEXT_NEUTRAL)

    def test_dashboard(self):
        request = self.factory.get('/dashboard')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard(self):
        request = self.factory.get('/leaderboard')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = leaderboard(request)
        self.assertEqual(response.status_code, 200)

    def test_progress(self):
        request = self.factory.get('/progress')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.progress(request)
        self.assertEqual(response.status_code, 200)

    def test_response(self):
        request = self.factory.get('/response/')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.response(request, self.task.id)
        self.assertEqual(response.status_code, 200)

    def test_response_post(self):
        payload = {
            self.question_1.id: '4',
            self.question_2.id: str(self.question_2.traffic_light_sad_value),
            self.question_3.id: 'textresponse',
            'clicked': ''
        }
        request = self.factory.post('/response', payload)
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = views.response(request, self.task.id)
        self.assertEqual(response.status_code, 302)
