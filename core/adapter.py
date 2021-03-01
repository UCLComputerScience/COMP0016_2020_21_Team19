from invitations.app_settings import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up

# Code credits here to django-allauth
class UserInvitationsAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if hasattr(request, 'session') and request.session.get(
                'account_verified_email'):
            return True
        elif app_settings.INVITATION_ONLY and request.META['PATH_INFO'] != "/create_organisation":
            # Site is ONLY open for invites
            return False
        else:
            # Site is open to signup
            return True

    def get_user_signed_up_signal(self):
        return user_signed_up