from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from core.views import dashboard, leaderboard
from respondent.models import Respondent
from surveyor.models import Surveyor

class CoreViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')

    def test_dashboard_not_logged_in(self):
        request = self.factory.get('/dashboard')
        request.user = self.user
        request.user = AnonymousUser()
        response = dashboard(request)
        self.assertEqual(response.status_code, 302) # 302 = redirected to login

    def test_leaderboard_not_logged_in(self):
        request = self.factory.get('/leaderboard')
        request.user = self.user
        request.user = AnonymousUser()
        response = dashboard(request)
        self.assertEqual(response.status_code, 302) # 302 = redirected to login

    def test_dashboard_surveyor(self):
        request = self.factory.get('/dashboard')
        Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_respondent(self):
        request = self.factory.get('/dashboard')
        Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_surveyor(self):
        request = self.factory.get('/leaderboard')
        Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = leaderboard(request)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_respondent(self):
        request = self.factory.get('/leaderboard')
        Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = leaderboard(request)
        self.assertEqual(response.status_code, 200)