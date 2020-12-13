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

from Interviewee import views as interviewee
from Interviewer import views as interviewer

urlpatterns = [
    path('', interviewee.login, name='login'),
    
    # INTERVIEWEE
    url(r'^interviewee@(?P<pk>\d+)/?$', interviewee.dashboard, name='interviewee_dashboard'),
    url(r'^interviewee@(?P<pk>\d+)/leaderboard/?$', interviewee.leaderboard, name='interviewee_leaderboard'),

    # INTERVIEWER
    url(r'^interviewer@(?P<pk>\d+)/?$', interviewer.dashboard, name='interviewer_dashboard'),
    url(r'^interviewer@(?P<pk>\d+)/leaderboard/?$', interviewer.leaderboard, name='interviewer_leaderboard'),
    
    path('admin/', admin.site.urls),
    # path('Interviewee/leaderboard/', interviewee.leaderboard, name='leaderboard'),
    path('Interviewee/response/', interviewee.response, name="response"),

    path('Interviewer/', interviewer.dashboard, name="dashboard"),
    path('Interviewer/leaderboard/', interviewer.leaderboard, name="leaderboard"),
    path('Interviewer/task_overview/', interviewer.task_overview, name="task_overview"),
    path('Interviewer/new_task', interviewer.new_task, name="new_task")
]
