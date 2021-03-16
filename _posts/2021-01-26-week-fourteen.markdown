---
layout: post
title:  "Week Fourteen: Authentication"
date:   2021-01-26
categories: authentication, privacy, groups
name: Team 19
---

## Authentication

This week, a large proportion of our focus has been directed at implementing user authentication for our web app. Our client had mentioned the use of a third-party access management solution called Keycloak, though given none of the three of us on the team had any prior web development experience whatsoever, we decided it wise to spend some time investigating alternatives before committing to a single solution.

### Requirements

Prior to researching our solution, we compiled a list of requirements for what we'd be looking for in an authentication system:

- Support for external authentication providers (such that we could implement an SSO-like login with social accounts)
- The use of standard protocols (such as OAuth 2.0, OIDC)
- Good documentation or resources available
- Traditional Email/Password Authentication (opening signup to those that wanted a traditional authentication system)

### Research

Having consolidated our list of requirements, we all set out investigating third party solutions which we could integrate with our given solution.

Developing our own authentication system was never an option for us - it would have introduced a great deal of unnecessary work which would have likely resulted in an insecure/less secure system compared to the third party implementations that already existed. Moreover, our security module lead had been very clear and specific in guidance to our class on this matter: *"never implement your own security"*.

We came across two main candidates:

1. **Keycloak**: Keycloak ticked all the boxes of the requirements above, supported identity brokering and had an enormous range of identity providers to choose from. Everything looked great until we tried to implement a prototype using Keycloak. It was at this stage that we realised just how niche the combination of docker-compose, permanent database volumes, django and keycloak really was, and we couldn't find any resources which bore any real resemblence to the problem that we faced ahead of us. Of course, this didn't stop us from attempting to integrate the solution regardless, but after a few days of documentation diving and experimentation, the team and I finally gave up the ghost and put our Keycloak branch on the back-burner.

2. **Django-Allauth**: Although we actually intended to look for alternatives to Keycloak as part of this research stage anyway, it was actually in our struggle to implement prototypes of Keycloak that we came across `django-allauth`. This was a fantastic, well-maintained package that also ticked all of the boxes that we had but also included more attractive features (see the section below).

### Djago-Allauth

As a native third-party extension, [django allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) was immediately simpler to integrate than Keycloak was. We found that in the period of a day with it, we'd implemented more functionality than in the preceding six attempting to integrate Keycloak. In addition satisfying the criterion above, allauth had a few other features which we recognised would be immensely valuable to us in the future, including: 

- The full forgotten password flow
- The capacity for integration with email invitations
- The ability to modify their default behaviour using an extendable `DefaultAccountAdapter`
- Default authentication templates
- Straightforward integration with social account providers

### Integration of Allauth

To integrate our solution with the new authentication provider, we had to take the following steps:

1. Add `django-allauth` to the bottom of our `requirements.txt`
2. Add the following to `settings.py`:

{% raw %}
```python3
...

INSTALLED_APPS = [
    ...

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

...

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
] 

...

SITE_ID = 1
```
{% endraw %}

3. Get the account templates from allauth.

Before starting to properly integrate allauth, it's worth noting that allauth has its own `User` type which you may need to integrate (as we did) with our existing `Surveyor` and `Respondent` models, where we tied instances of both models to instances of the new `User` model, resulting in a change to our database schema. Moreover, instead of implementing your own sign up and login templates, modify the ones that allauth has already given to you. Allauth works with these templates by default and when you later configure social account identity providers, it expects the link clicks to come from these templates.

After integrating the above, the remainder of the process to setting this up involves following the standard django MVT pattern: create a corresponding view for your new templates (and the forms to display in these new templates). There already exist default `Signup` views and forms for you to override, as we did, if necessary. In the case of the `SignupForm` you simply needed to inherit the default and override the `save` method, like so in `forms.py`: 

{% raw %}

```python3
class SurveyorSignupForm(SignupForm):
    firstname = forms.CharField(max_length=30, min_length=1)
    surname = forms.CharField(max_length=30, min_length=1)

    def save(self, request):
        user = super(SurveyorSignupForm, self).save(request)

        surveyor = Surveyor(
            user = user,
            firstname=self.cleaned_data.get('firstname'),
            surname=self.cleaned_data.get('surname')
        )

        surveyor.save()

        # Return the django-allauth User instance, 
        # otherwise we will get an error.
        return surveyor.user
```

{% endraw %}

The corresponding view in `views.py` would look something like:

{% raw %}
```python3
class RespondentSignupView(SignupView):
    template_name = 'account/signup_respondent.html'

    form_class = RespondentSignupForm

    view_name = 'respondent_signup'

    # I don't use them, but you could override them
    # (N.B: the following values are the default)
    success_url = 'respondent@1/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        ret = super(RespondentSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret
```
{% endraw %}

For more details of our first implementation, see commits `01fb80b45fba293103c53478658427bd5702a8ef` and `273e4649e870ac2eb1f3165af88141e29e2486b9` in our [repo](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19).

## Next Week

Now that we have got a baseline version of authentication working, next week is all about optimising the integration between our platform and allauth:

- Styling default login screens
- Customising the login process
- Implementing new functionalities