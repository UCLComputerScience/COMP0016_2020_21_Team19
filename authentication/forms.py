from allauth.account.forms import SignupForm, LoginForm
from django import forms


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
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('surname')
        user.save()
        return user


class AuthenticationLoginForm(LoginForm):
    class Meta:
        field_order = ['login', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""

    def login(self, *args, **kwargs):
        return super(AuthenticationLoginForm, self).login(*args, **kwargs)
