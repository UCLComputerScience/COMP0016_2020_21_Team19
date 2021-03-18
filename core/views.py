from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import respondent
import surveyor
from respondent.models import Respondent
from surveyor.models import Surveyor
from .forms import OrganisationSignupForm


def create_organisation(request):
    if request.method == 'POST':
        form = OrganisationSignupForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)
            request.session['organisation_name'] = organisation.name
            return HttpResponseRedirect(reverse('authentication-signup'))
        else:
            raise Http404("Invalid organisation name")
    elif request.method == 'GET':
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
