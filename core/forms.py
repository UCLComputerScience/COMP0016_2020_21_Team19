from django import forms

from surveyor.models import Organisation


class OrganisationSignupForm(forms.ModelForm):
    """
    Form used to create new organisations.
    """

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
