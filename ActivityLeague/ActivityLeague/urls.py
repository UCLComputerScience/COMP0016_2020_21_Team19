from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from respondent import views as respondent
from surveyor import views as surveyor
from core import views as core
from django.http.response import HttpResponseRedirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: HttpResponseRedirect('/accounts/login')),
    path('accounts/', include('allauth.urls')),
    
    # core
    url(r'^dashboard/?$', core.dashboard, name='dashboard'),
    url(r'^leaderboard/?$', core.leaderboard, name='leaderboard'),
    url(r'^response/(?P<id>[0-9a-f-]+)/?$', respondent.response, name='response'),
    url(r'^progress/?$', respondent.progress, name='respondent_progress'),

    # surveyor
    url(r'^task/(?P<pk_task>[0-9a-f-]+)/?$', surveyor.task_overview, name='task_overview'),
    url(r'^new_group/?$', surveyor.new_group, name='new_group'),
    url(r'^groups/?$', surveyor.groups, name='groups'),
    url(r'^history/?$', surveyor.history, name='history'),
    url(r'^new_task/?$', surveyor.new_task, name='new_task'),
    url(r'^manage_group/(?P<pk_group>[0-9a-f-]+)/?$', surveyor.manage_group, name='manage_group'),
    url(r'^users/?$', surveyor.users, name='users'),
    url(r'^user/(?P<pk_user>[0-9a-f-]+)/response/(?P<pk_task>[0-9a-f-]+)/?$', surveyor.user_response, name='user_response'),
    url(r'^user/(?P<pk_user>[0-9a-f-]+)/?$', surveyor.user_progress, name='user_progress'),

]
