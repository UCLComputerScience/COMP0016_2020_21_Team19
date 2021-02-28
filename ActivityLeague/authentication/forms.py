from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm, LoginForm

from surveyor.models import Surveyor
from respondent.models import Respondent, GroupRespondent
from core.models import SurveyorOrganisation, UserInvitation

class AuthenticationSignupForm(SignupForm):
    firstname = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    
    surname = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['firstname'].label = ""
        self.fields['surname'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

    def save(self, request):
        user = super(AuthenticationSignupForm, self).save(request)
        invite = UserInvitation.objects.get(email=self.cleaned_data.get('email'))

        if invite.is_respondent:
            group = invite.group
            respondent = Respondent(
                user=user,
                firstname=self.cleaned_data.get('firstname'),
                surname=self.cleaned_data.get('surname')
            )
            respondent.save()
            group_respondent = GroupRespondent(
                group=group,
                respondent=respondent
            )
            group_respondent.save()
        else:
            organisation = invite.organisation
            surveyor = Surveyor(
                user=user,
                firstname=self.cleaned_data.get('firstname'),
                surname=self.cleaned_data.get('surname')
            )
            surveyor.save()
            surveyor_organisation = SurveyorOrganisation(
                surveyor=surveyor,
                organisation=organisation
            )
            surveyor_organisation.save()
        
        return user

class AuthenticationLoginForm(LoginForm):
    class Meta:
        field_order = ['login', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""
        # self.fields["forgot"].class
    
    def login(self, *args, **kwargs):
        return super(AuthenticationLoginForm, self).login(*args, **kwargs)