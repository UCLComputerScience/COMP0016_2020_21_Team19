from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm

from .models import *

class RespondentSignupForm(SignupForm):
    firstname = forms.CharField(max_length=30, min_length=1)
    surname = forms.CharField(max_length=30, min_length=1)

    def save(self, request):
        user = super(RespondentSignupForm, self).save(request)

        respondent = Respondent(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            surname=self.cleaned_data.get('surname')
        )
        respondent.save()

        return respondent.user