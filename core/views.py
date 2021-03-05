from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import respondent
import surveyor
from respondent.models import Respondent
from surveyor.models import Surveyor
from .forms import OrganisationSignupForm


class OrganisationSignup(SignupView):
    template_name = 'account/create-organisation.html'
    form_class = OrganisationSignupForm
    redirect_field_name = 'dashboard'
    view_name = 'create-organisation'

    def get_context_data(self, **kwargs):
        ret = super(OrganisationSignup, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


@login_required(login_url='/accounts/login/')
def dashboard(request):
    if Surveyor.objects.filter(user=request.user):
        return surveyor.views.dashboard(request)
    elif Respondent.objects.filter(user=request.user):
        return respondent.views.dashboard(request)
    else:
        return HttpResponse("Hello")


@login_required(login_url='/accounts/login/')
def leaderboard(request):
    if Surveyor.objects.filter(user=request.user):
        return surveyor.views.leaderboard(request)
    elif Respondent.objects.filter(user=request.user):
        return respondent.views.leaderboard(request)
