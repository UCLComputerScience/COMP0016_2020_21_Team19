from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
import datetime
from django.utils import timezone

import respondent
import surveyor
from respondent.models import Respondent
from surveyor.models import Surveyor, Organisation
from .forms import OrganisationSignupForm
from .models import UserInvitation
from authentication.views import AuthenticationSignup
from invitations.views import accept_invitation, AcceptInvite


def create_organisation(request):
    if request.method == 'POST':
        form = OrganisationSignupForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)
            request.session['organisation_name'] = organisation.name
            return HttpResponseRedirect(reverse('authentication-signup'))
    form = OrganisationSignupForm()
    return render(request, 'account/create-organisation.html', {'form': form})


@login_required(login_url='/accounts/login/')
def dashboard(request):
    if Surveyor.objects.filter(user=request.user):
        return surveyor.views.dashboard(request)
    elif Respondent.objects.filter(user=request.user):
        return respondent.views.dashboard(request)
    else:
        raise Http404("You were not invited!")


@login_required(login_url='/accounts/login/')
def leaderboard(request):
    if Surveyor.objects.filter(user=request.user):
        return surveyor.views.leaderboard(request)
    elif Respondent.objects.filter(user=request.user):
        return respondent.views.leaderboard(request)
