from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404

from core.views import *
from core.models import *
from respondent.models import *
from surveyor.models import *

"""
Testing invalid GET requests is unnecessary - it is the same as testing Django's
internal get_object_or_404 which is assumed to work.
"""


class CoreViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@email.com', password='top_secret')

    def test_create_organisation_get(self):
        """
        The `/create-organisation` page should be open to anonymous users.
        """
        request = self.factory.get(reverse('create-organisation'))
        request.user = AnonymousUser()
        response = create_organisation(request)
        self.assertEqual(response.status_code, 200)

    def test_create_organisation_post_valid(self):
        """
        A valid `POST` to `/create-organisation` should redirect to `/accounts/signup`.
        """
        payload = {'name': 'Organisation'}
        request = self.factory.post(reverse('create-organisation'), payload)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()
        response = create_organisation(request)
        self.assertEqual(response.status_code, 302)

    def test_create_organisation_post_invalid(self):
        """
        An invalid `POST` to `/create-organisation` should return a 404 error.
        """
        payload = {'name': ''}
        request = self.factory.post(reverse('create-organisation'), payload)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()
        with self.assertRaises(Http404, msg='Invalid organisation name'):
            response = create_organisation(request)

    def test_dashboard_not_logged_in(self):
        """
        The `/dashboard` page should redirect to `/accounts/login` if the user is not logged in.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = AnonymousUser()
        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    def test_leaderboard_not_logged_in(self):
        """
        The `/leaderboard` page should redirect to `/accounts/login` if the user is not logged in.
        """
        request = self.factory.get(reverse('leaderboard'))
        request.user = self.user
        request.user = AnonymousUser()
        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_surveyor(self):
        """
        The `/dashboard` page should be open to Surveyors.
        """
        request = self.factory.get(reverse('dashboard'))
        Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_respondent(self):
        """
        The `/dashboard` page should be open to Respondents.
        """
        request = self.factory.get(reverse('dashboard'))
        Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_uninvited(self):
        """
        The `/dashboard` should return a 404 error if the user is logged in
        but neither a Surveyor or Respondent.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        with self.assertRaises(Http404, msg='You were not invited!'):
            response = dashboard(request)

    def test_leaderboard_surveyor(self):
        """
        The `/dashboard` page should be open to Surveyors.
        """
        request = self.factory.get(reverse('leaderboard'))
        Surveyor.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = leaderboard(request)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_respondent(self):
        """
        The `/dashboard` page should be open to Respondents.
        """
        request = self.factory.get(reverse('leaderboard'))
        Respondent.objects.create(user=self.user, firstname='Jacob', surname='Testuser')
        request.user = self.user
        login = self.client.login(username='jacob@email.com', password='top_secret')
        response = leaderboard(request)
        self.assertEqual(response.status_code, 200)
