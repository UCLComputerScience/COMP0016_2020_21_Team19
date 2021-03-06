from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up
from invitations.app_settings import app_settings
from django.urls import reverse
from urllib import parse


# Code credits here to django-allauth
class UserInvitationsAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if hasattr(request, 'session') and request.session.get('account_verified_email'):
            return True
        elif app_settings.INVITATION_ONLY:
            http_referer = request.META.get('HTTP_REFERER')
            print("Path:", parse.urlparse(http_referer).path)
            print(reverse('account_signup'))
            print()
            return parse.urlparse(http_referer).path == reverse('create-organisation') or parse.urlparse(http_referer).path in reverse('account_signup')
        else:
            # Site is open to signup
            return True

    def get_user_signed_up_signal(self):
        return user_signed_up
