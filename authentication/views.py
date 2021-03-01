from django.shortcuts import render
from .forms import AuthenticationSignupForm
from allauth.account.views import SignupView


class AuthenticationSignup(SignupView):
    template_name = 'account/signup.html'
    form_class = AuthenticationSignupForm
    redirect_field_name = 'dashboard'
    view_name = 'sign_up'

    def get_context_data(self, **kwargs):
        ret = super(AuthenticationSignup, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret
