from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import datetime
from surveyor.models import Surveyor, Task
from respondent.models import Respondent, GroupRespondent

@login_required(login_url='/accounts/login/')
def dashboard(request):
    if Surveyor.objects.filter(user=request.user):
        user = get_object_or_404(Surveyor, user=request.user)
        return render(request, 'surveyor_dashboard.html', {'user' : user})
    elif Respondent.objects.filter(user=request.user):
        user = get_object_or_404(Respondent, user=request.user)
        # get the groups that this user is a part of
        groups = GroupRespondent.objects.filter(respondent=user).values_list('group')
        # only get the tasks which are assigned to a group the user is a part of
        tasks = Task.objects.filter(group__in=groups)
        now = datetime.datetime.now()
        for task in tasks:
            # creating a combined DateTime object to allow for "Time Remaining" to be shown
            task.due_dt = datetime.datetime.combine(task.due_date, task.due_time)
            until = task.due_dt - now
            # working out time left to determine color of "Time Remaining"
            task.color = "red" if until < datetime.timedelta(days=1) else "orange" if until < datetime.timedelta(days=2) else "darkgreen"
        return render(request, 'respondent_dashboard.html', {'user' : user, 'tasks' : tasks, 'now' : now})

@login_required(login_url='/accounts/login/')
def leaderboard(request):
    if Surveyor.objects.filter(user=request.user):
        user = get_object_or_404(Surveyor, user=request.user)
        return render(request, 'surveyor_leaderboard.html', {'user' : user})
    elif Respondent.objects.filter(user=request.user):
        user = get_object_or_404(Respondent, user=request.user)
        return render(request, 'respondent_leaderboard.html', {'user' : user})
    