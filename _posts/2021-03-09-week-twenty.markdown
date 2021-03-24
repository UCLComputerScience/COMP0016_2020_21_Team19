---
layout: post
title:  "Week Twenty: Feature Requests, Responsiveness and User Guides"
date:   2021-03-09
categories: enhancements, project, manual, templates, sso, responsiveness
name: Team 19
---

Over the course of the last week, we've focused on going above and beyond the functionalities in our requirements and implement features (some coming from our own intuitition, most from client feature requests), and completed the manuals for our project: the user manual, deployment manual and a getting started tutorial for the platform.

## New Functionalities

#### SSO (Google)

We started this week by implementing Single Sign-On authentication through Google using our authentication dependency `django-allauth`. To implement this, we first need to configure our `settings.py` to install the Google socialaccount provider, and enable it for use in django-allauth. I've included the relevant lines that need to be included below:

```python3
# settings.py

INSTALLED_APPS = [
 ...
 ‘social_app’,  

 ‘allauth’,
 ‘allauth.account’,
 ‘allauth.socialaccount’,
 ‘allauth.socialaccount.providers.google’,
]

...

AUTHENTICATION_BACKENDS = (
 ‘django.contrib.auth.backends.ModelBackend’,
 ‘allauth.account.auth_backends.AuthenticationBackend’,
)

...

SITE_ID = 1
LOGIN_REDIRECT_URL = ‘/’ # this is the path of wherever you want the user to go after they've logged in.

...

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

```

After you've configured the project settings, the next step that we need to follow is to include the default allauth project urls in `urls.py` (if you haven't done so already using allauth authentication): 

```python3

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(‘admin/’, admin.site.urls),
    path(‘accounts/’, include(‘allauth.urls’)),

    ...
]
```

And now go to the template that you usually use for logins (we use the standard allauth templates `/accounts/login.html`) and loop over the social account providers that you have configured to work with your project outside of the standard login form in the template:

```html
...

{% load account socialaccount %}

...

{% get_providers as socialaccount_providers %}

  ...

  {% if socialaccount_providers %}
  <div class="socialaccount_ballot mt-2">
    {% for provider in socialaccount_providers %}
      <a title="{{ provider.name }}" class="socialaccount_provider sb sb-m-2 sb-{{ provider.id }}" href="{% provider_login_url provider.id process="login" %}">
        Sign in with {{ provider.id | title }}
      </a>
    {% endfor %}
  </div>
  {% endif %}

  ...

```

Opening this template in a browser should now show an option to Sign In with Google. Clicking on this won't work just yet though, we still need to register our application with Google in order to enable this.

To set up OAuth on Google, navigate to the [Google Developers Console](https://console.developers.google.com), head to the **Dashboard** and create a new project (if you've got a project already, click on this in the top left corner of the page and the create a new project button is here). Give your project a name, and press **Continue**. Once you've done this, head back to the **Dashboard**, where on the left-hand side you'll see a link to **Credentials**. Click on this tab, and then click on the button called **Create Credentials** when it appears. This should render a drop-down, and when it appears, select **OAuth Client ID** from the list (this is what we are going to need to proceed with the SSO).

The tab now open will contain a tab for **OAuth Consent Screen**. This needs to be completed, and without it your application will not obtain the necessary credentials from the Google Developers Console to allow SSO authentication. Assuming that you're not a Google Workspace user, the only option from the next page that you can select is **External**, so go ahead and select this and head to the next page.

![OAuth Consent Screen](/COMP0016_2020_21_Team19/assets/google_oauth_consent_screen.png)


For more information and detail about the process of setting up Google SSO, we found the [allauth docs](https://django-allauth.readthedocs.io/en/latest/providers.html) and [this tutorial](https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5) to be particularly helpful.

#### Dark Mode

#### Manage Organisation

#### Seed and Load Templates

#### Delete Tasks

## Responsiveness

## Guides

#### User Manual

#### Deployment Manual

#### Getting Started Guide

## Integration/End to End Testing

