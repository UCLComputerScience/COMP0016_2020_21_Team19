from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from surveyor.models import Surveyor
from respondent.models import Respondent

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        if Surveyor.objects.filter(user=request.user):
            path = "/surveyor@1"
        elif Respondent.objects.filter(user=request.user):
            path = "/respondent@1"
        else:
            raise Exception("User type not expected.")
        return path.format(username=request.user.username)