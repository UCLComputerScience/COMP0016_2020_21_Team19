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

from Interviewee import views as interviewee
from Interviewer import views as interviewer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', interviewee.login, name='login'),
    
    path('Interviewee', interviewee.dashboard, name='dashboard'),
    path('Interviewee/leaderboard', interviewee.leaderboard, name='leaderboard'),
    path('Interviewee/response', interviewee.response, name="response"),

    path('Interviewer', interviewer.dashboard, name="dashboard"),
    path('Interviewer/leaderboard', interviewer.leaderboard, name="leaderboard"),
    path('Interviewer/task_overview', interviewer.task_overview, name="task_overview"),
    path('Interviewer/new_task', interviewer.new_task, name="new_task")
]
