from django.conf.urls import url
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls import include, path

from authentication import views as authentication
from core import views as core
from respondent import views as respondent
from surveyor import views as surveyor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: HttpResponseRedirect('/accounts/login')),

    url(r'^accounts/signup/?$', authentication.AuthenticationSignup.as_view()),
    path('accounts/', include('allauth.urls')),

    url(r'^invitations/', include('invitations.urls', namespace='invitations')),

    # core
    url(r'^dashboard/?$', core.dashboard, name='dashboard'),
    url(r'^leaderboard/?$', core.leaderboard, name='leaderboard'),
    url(r'^create-organisation/?$', core.OrganisationSignup.as_view(), name='create-organisation'),

    # respondent
    url(r'^response/(?P<id>[0-9a-f-]+)/?$', respondent.response, name='response'),
    url(r'^progress/?$', respondent.progress, name='respondent_progress'),

    # surveyor
    url(r'^task/(?P<pk_task>[0-9a-f-]+)/?$', surveyor.task_overview, name='task_overview'),
    url(r'^new-group/?$', surveyor.new_group, name='new-group'),
    url(r'^groups/?$', surveyor.groups, name='groups'),
    url(r'^history/?$', surveyor.history, name='history'),
    url(r'^new-task/?$', surveyor.new_task, name='new-task'),
    url(r'^manage-group/(?P<pk_group>[0-9a-f-]+)/?$', surveyor.manage_group, name='manage-group'),
    url(r'^users/?$', surveyor.users, name='users'),
    url(r'^user/(?P<pk_user>[0-9a-f-]+)/response/(?P<pk_task>[0-9a-f-]+)/?$', surveyor.user_response,
        name='user_response'),
    url(r'^user/(?P<pk_user>[0-9a-f-]+)/?$', surveyor.user_progress, name='user_progress'),

]
