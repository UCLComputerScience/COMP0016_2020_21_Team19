"""ActivityLeague URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from respondent import views as respondent
from surveyor import views as surveyor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', respondent.login, name='login'),
    
    # respondent
    url(r'^respondent@(?P<pk>\d+)/?$', respondent.dashboard, name='respondent_dashboard'),
    url(r'^respondent@(?P<pk>\d+)/leaderboard/?$', respondent.leaderboard, name='respondent_leaderboard'),
    url(r'^respondent@(?P<pk>\d+)/response/?$', respondent.response, name='response'),

    # surveyor
    url(r'^surveyor@(?P<pk>\d+)/?$', surveyor.dashboard, name='surveyor_dashboard'),
    url(r'^surveyor@(?P<pk>\d+)/new_group/?$', surveyor.new_group, name='new_group'),
    url(r'^surveyor@(?P<pk>\d+)/leaderboard/?$', surveyor.leaderboard, name='surveyor_leaderboard'),
    url(r'^surveyor@(?P<pk>\d+)/new_task/?$', surveyor.new_task, name='new_task'),
    url(r'^surveyor@(?P<pk>\d+)/task_overview/?$', surveyor.task_overview, name='task_overview')
    
    # path('respondent/leaderboard/', respondent.leaderboard, name='leaderboard'),

    # path('surveyor/', surveyor.dashboard, name="dashboard"),
    # path('surveyor/leaderboard/', surveyor.leaderboard, name="leaderboard"),
    # path('surveyor/task_overview/', surveyor.task_overview, name="task_overview"),
    # path('surveyor/new_task', surveyor.new_task, name="new_task")
]
