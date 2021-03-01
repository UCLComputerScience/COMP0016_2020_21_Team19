import uuid
import datetime

from django.db import models

from django.conf import settings
from django.contrib.sites.models import Site

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from invitations import signals
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings
from invitations.base_invitation import AbstractBaseInvitation

from surveyor.models import Surveyor, Group, GroupSurveyor
from respondent.models import GroupRespondent

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    admin = models.ForeignKey(Surveyor, on_delete=models.CASCADE)


class SurveyorOrganisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE)


class UserInvitation(AbstractBaseInvitation):
    email = models.EmailField(unique=True, verbose_name=_('e-mail address'),
                              max_length=app_settings.EMAIL_MAX_LENGTH)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    organisation = models.ForeignKey(Organisation, blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    is_respondent = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, email, inviter=None, organisation=None, group=None, is_respondent=False, **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter,
            organisation=organisation,
            group=group,
            is_respondent=is_respondent,
            **kwargs)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        surveyor = Surveyor.objects.get(user=self.inviter)

        if not self.is_respondent:
            self.organisation = SurveyorOrganisation.objects.get(surveyor=surveyor).organisation
        
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)

        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)

    def __str__(self):
        return "Invite: {0}".format(self.email)


# here for backwards compatibility, historic allauth adapter
if hasattr(settings, 'ACCOUNT_ADAPTER'):
    if settings.ACCOUNT_ADAPTER == 'invitations.models.InvitationsAdapter':
        from allauth.account.adapter import DefaultAccountAdapter
        from allauth.account.signals import user_signed_up

        class InvitationsAdapter(DefaultAccountAdapter):

            def is_open_for_signup(self, request):
                if hasattr(request, 'session') and request.session.get(
                        'account_verified_email'):
                    return True
                elif app_settings.INVITATION_ONLY is True:
                    # Site is ONLY open for invites
                    return False
                else:
                    # Site is open to signup
                    return True

            def get_user_signed_up_signal(self):
                return user_signed_up