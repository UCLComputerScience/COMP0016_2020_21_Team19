from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import datetime
from surveyor.models import Surveyor, Task
from respondent.models import Respondent, GroupRespondent
from .forms import OrganisationSignupForm
from allauth.account.views import SignupView
import surveyor
import respondent


class OrganisationSignup(SignupView):
    template_name = 'account/create_organisation.html'
    form_class = OrganisationSignupForm
    redirect_field_name = 'dashboard'
    view_name = 'create_organisation'

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

@login_required(login_url='/accounts/login/')
def leaderboard(request):
    if Surveyor.objects.filter(user=request.user):
        return surveyor.views.leaderboard(request)
    elif Respondent.objects.filter(user=request.user):
        return respondent.views.leaderboard(request)