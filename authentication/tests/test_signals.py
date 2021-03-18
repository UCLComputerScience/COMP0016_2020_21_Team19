from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from allauth.account.signals import user_signed_up

from core.views import *
from authentication.models import *
from core.models import *
from respondent.models import *
from surveyor.models import *


class AuthenticationSignalsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()
        self.surveyor_user = User.objects.create_user(username='jacob', email='jacob@email.com', password='top_secret', first_name='Jacob', last_name='Doe')
        self.respondent_user = User.objects.create_user(username='john', email='john@doe.com', password='top_secret', first_name='John', last_name='Doe')


    def test_organisation_created(self):
        """
        An organisation should be created if a Surveyor signs up
        through `/create-organisation`.
        """
        request = self.factory.get(reverse('authentication-signup'))
        self.middleware.process_request(request)
        request.session['organisation_name'] = 'Organisation'
        request.session.save()
        user_signed_up.send(sender=self.surveyor_user.__class__, request=request, user=self.surveyor_user)
        self.assertTrue(Organisation.objects.filter(name='Organisation').exists())


    def test_signup_from_invite_respondent(self):
        """
        A Respondent object should be created if a Respondent signs up
        by accepting an invite.
        """
        group = Group.objects.create(name='Group')
        UserInvitation.create(self.respondent_user.email, group=group, is_respondent=True)
        request = self.factory.get(reverse('authentication-signup'))
        self.middleware.process_request(request)
        request.session.save()
        user_signed_up.send(sender=self.respondent_user.__class__, request=request, user=self.respondent_user)
        self.assertTrue(Respondent.objects.filter(firstname=self.respondent_user.first_name).exists())


    def test_signup_from_invite_surveyor(self):
        """
        A Surveyor object should be created if a Respondent signs up
        by accepting an invite.
        """
        organisation = Organisation.objects.create(name='Organisation')
        UserInvitation.create(self.surveyor_user.email, organisation=organisation, is_respondent=False)
        request = self.factory.get(reverse('authentication-signup'))
        self.middleware.process_request(request)
        request.session.save()
        user_signed_up.send(sender=self.surveyor_user.__class__, request=request, user=self.surveyor_user)
        self.assertTrue(Surveyor.objects.filter(firstname=self.surveyor_user.first_name).exists())

    def test_signup_uninvited(self):
        """
        A 404 error should be returned if a user who has not been invited
        tries to sign up.
        """
        request = self.factory.get(reverse('authentication-signup'))
        self.middleware.process_request(request)
        request.session.save()
        with self.assertRaises(Http404):
            user_signed_up.send(sender=self.surveyor_user.__class__, request=request, user=self.surveyor_user)