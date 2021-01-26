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
from django.urls import include, path
from django.conf.urls import url

from respondent import views as respondent
from surveyor import views as surveyor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', respondent.login, name='login'),
    path('register/', respondent.register, name='register'),
    path('accounts/', include('allauth.urls')),

    # sign up
    url(r'^accounts/signup/surveyor/', surveyor.surveyor_signup, name='surveyor_signup'),
    url(r'^accounts/signup/respondent/', respondent.respondent_signup, name='respondent_signup'),
    
    # respondent
    url(r'^respondent@(?P<pk>\d+)/?$', respondent.dashboard, name='respondent_dashboard'),
    url(r'^respondent@(?P<pk>\d+)/leaderboard/?$', respondent.leaderboard, name='respondent_leaderboard'),
    url(r'^respondent@(?P<pk>\d+)/get_respondent_leaderboard_json$', respondent.get_respondent_leaderboard_json, name='get_respondent_leaderboard_json'),
    url(r'^respondent@(?P<pk>\d+)/get_respondent_leaderboard_groups_json$', respondent.get_respondent_leaderboard_groups_json, name='get_respondent_leaderboard_groups_json'),
    url(r'^respondent@(?P<pk>\d+)/response(?P<id>\d+)/?$', respondent.response, name='response'),
    url(r'^respondent@(?P<pk>\d+)/progress/?$', respondent.progress, name='respondent_progress'),
    url(r'^respondent@(?P<pk>\d+)/get_progress_json$', respondent.get_progress_json, name='get_progress_json'),

    # surveyor
    url(r'^surveyor@(?P<pk>\d+)/?$', surveyor.dashboard, name='surveyor_dashboard'),
    url(r'^surveyor@(?P<pk>\d+)/task@(?P<pk_task>\d+)/?$', surveyor.task_overview, name='task_overview'),
    url(r'^surveyor@(?P<pk>\d+)/task@(?P<pk_task>\d+)/get_questions_json?$', surveyor.get_questions_json, name='get_questions_json'),
    url(r'^surveyor@(?P<pk>\d+)/get_graphs_and_leaderboards_json$', surveyor.get_graphs_and_leaderboards_json, name='get_graphs_and_leaderboards_json'),
    url(r'^surveyor@(?P<pk>\d+)/get_tasks_json$', surveyor.get_tasks_json, name='get_tasks_json'),
    url(r'^surveyor@(?P<pk>\d+)/get_leaderboard_json$', surveyor.get_leaderboard_json, name='get_leaderboard_json'),
    url(r'^surveyor@(?P<pk>\d+)/get_leaderboard_groups_json$', surveyor.get_leaderboard_groups_json, name='get_leaderboard_groups_json'),
    url(r'^surveyor@(?P<pk>\d+)/new_group/?$', surveyor.new_group, name='new_group'),
    url(r'^surveyor@(?P<pk>\d+)/leaderboard/?$', surveyor.leaderboard, name='surveyor_leaderboard'),
    url(r'^surveyor@(?P<pk>\d+)/new_task/?$', surveyor.new_task, name='new_task')
    
    # path('respondent/leaderboard/', respondent.leaderboard, name='leaderboard'),

    # path('surveyor/', surveyor.dashboard, name="dashboard"),
    # path('surveyor/leaderboard/', surveyor.leaderboard, name="leaderboard"),
    # path('surveyor/task_overview/', surveyor.task_overview, name="task_overview"),
    # path('surveyor/new_task', surveyor.new_task, name="new_task")
]
