from allauth.account.forms import SignupForm
from django import forms

from surveyor.models import Organisation
from surveyor.models import Surveyor


class OrganisationSignupForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ('name',)
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Organisation Name'
                }
            )
        }