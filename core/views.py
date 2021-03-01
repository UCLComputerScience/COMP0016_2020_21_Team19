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

@login_required
def company_users(request):
    # Get users that are in the company's user database as well as users that have been invited
    company_users = CustomUser.objects.filter(company=request.user.company.id)
    Invitations = get_invitation_model()
    # I'm afraid this is going to get all invited users, not just those that belong to the company
    invited_users = Invitations.objects.filter()

    if request.method == 'POST':
        print(request.POST)
        invitees = request.POST['invitees']
        invitees = re.split(',', invitees)
        for invitee in invitees:
            Invitation = get_invitation_model()
            try:
                invite = Invitation.create(invitee, inviter=request.user)
                invite.send_invitation(request)
            except IntegrityError as e:
                print(type(e))
                print(dir(e))
                return render(request, "company_users.html", {
                    'message': e.args,
                    'company_users' : company_users,
                    'invited_users' : invited_users,
                    })

    
    return render(request, 'company_users.html', {
        'company_users' : company_users,
        'invited_users' : invited_users,
    })

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