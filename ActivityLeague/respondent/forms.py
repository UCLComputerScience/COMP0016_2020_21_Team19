from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm

from .models import *

class RespondentSignupForm(SignupForm):
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
        user = super(RespondentSignupForm, self).save(request)

        respondent = Respondent(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            surname=self.cleaned_data.get('surname')
        )
        respondent.save()

        return respondent.user