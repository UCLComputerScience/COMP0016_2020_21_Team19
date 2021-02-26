from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm, LoginForm

from surveyor.models import Surveyor
from respondent.models import Respondent

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
        pass
        # TODO: Handle signup of surveyor/repsondent based on email link click

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