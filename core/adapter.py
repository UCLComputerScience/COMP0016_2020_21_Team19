from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up
from invitations.app_settings import app_settings


class UserInvitationsAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-invitations.
    Restricts signup to new Surveyors and invited users only.
    """
    def is_open_for_signup(self, request):
        if hasattr(request, 'session') and request.session.get('account_verified_email'):
            return True
        elif app_settings.INVITATION_ONLY:
            return request.session.get('organisation_name')
        else:
            return True

    def get_user_signed_up_signal(self):
        return user_signed_up
