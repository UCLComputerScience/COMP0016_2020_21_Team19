from allauth.account.forms import SignupForm
from django import forms

from core.models import Organisation, SurveyorOrganisation
from surveyor.models import Surveyor


class OrganisationSignupForm(SignupForm):
    organisation_name = forms.CharField(max_length=50, min_length=1,
                                        widget=forms.TextInput(attrs={'placeholder': 'Organisation Name'}))

    firstname = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))

    surname = forms.CharField(max_length=30, min_length=1, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))

    field_order = ['organisation_name', 'email', 'firstname', 'surname', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['organisation_name'].label = ""
        self.fields['email'].label = ""
        self.fields['firstname'].label = ""
        self.fields['surname'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

    def save(self, request):
        user = super(OrganisationSignupForm, self).save(request)
        # Creating the Surveyor
        surveyor = Surveyor(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            surname=self.cleaned_data.get('surname')
        )
        surveyor.save()
        # Creating the Organisation
        organisation = Organisation(
            name=self.cleaned_data.get('organisation_name'),
            admin=surveyor
        )
        organisation.save()
        # Creating the SurveyorOrganisation
        surveyor_organisation = SurveyorOrganisation(
            organisation=organisation,
            surveyor=surveyor
        )
        surveyor_organisation.save()

        return user
