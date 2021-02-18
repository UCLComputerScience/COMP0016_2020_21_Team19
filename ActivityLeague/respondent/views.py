import datetime
import operator
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from surveyor.models import *
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required

import random

@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = get_object_or_404(Respondent, user=request.user)
    # get the groups that this user is a part of
    groups = GroupRespondent.objects.filter(respondent=user).values_list('group', flat=True)
    # only get the tasks which are assigned to a group the user is a part of
    tasks = Task.objects.filter(group__in=groups)
    tasks = list(filter(lambda task: not task_is_completed(request.user, task), tasks))
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
    user = get_object_or_404(Respondent, user=request.user)
    return render(request, 'respondent_leaderboard.html', {'user' : user})

@login_required(login_url='/accounts/login/')
def progress(request):
    user = get_object_or_404(Respondent, user=request.user)
    labels = get_progress_labels(request.user)
    scores = get_progress_values(request.user, labels)
    groups = get_groups(request.user)
    return render(request, 'respondent_progress_page.html', {'user' : user, 'labels': labels, 'scores': scores, 'groups': groups})

@login_required(login_url='/accounts/login/')
def get_progress_json(request):
    groups = get_groups(request.user)
    overall_labels = get_progress_labels(request.user)

    group_graphs = []
    overall_data = []
    for group in groups:
        group_labels = get_progress_labels(request.user, group=group)
        group_scores = get_progress_values(request.user, group_labels, group=group)
        group_title = group.name
        group_graphs.append({ 'title': group_title, 'labels': group_labels, 'scores': [get_chartjs_dict(group_scores)] })

        overall_data.append(get_chartjs_dict(group_scores))

    return JsonResponse(data={
        'overall': overall_data,
        'overall_labels': overall_labels,
        'groups': group_graphs
    })

def random_hex_colour():
    random_n = random.randint(0, 16777215)
    hex_number = format(random_n,'x')
    hex_number = '#' + hex_number
    return hex_number

def get_chartjs_dict(scores):
    return {'data': scores,
            'lineTension': 0,
            'backgroundColor': 'transparent',
            'borderColor': random_hex_colour(),
            'borderWidth': 4,
            'pointBackgroundColor': '#007bff'}

@login_required(login_url='/accounts/login/')
def response(request, id):
    user = get_object_or_404(Respondent, user=request.user)
    task = Task.objects.get(id=id)
    questions = Question.objects.filter(task=task)

    # form submitted
    if request.method == 'POST':
        dict = request.POST.items()
        # get a list of Question IDs for which the user clicked the link
        clicked = [x for x in request.POST.get('clicked').split(',')]
        current_date_time = timezone.now()
        for qid, data in dict:
            # don't need to process the csrf token or the array of clicked Question IDs
            if qid == 'csrfmiddlewaretoken' or qid == 'clicked':
                continue
            q = Question.objects.get(id=qid)
            link_clicked = qid in clicked
            if q.response_type == 1: # likert
                likert_dict = {
                    'strong_disagree' : 1,
                    'disagree' : 2,
                    'neutral' : 3,
                    'agree' : 4,
                    'strong_agree' : 5
                }
                Response.objects.create(question=q, respondent=user, value=likert_dict[data], date_time=current_date_time, link_clicked=link_clicked)
            elif q.response_type == 2: # traffic light
                tl_dict = {
                    'red' : 1,
                    'yellow' : 2,
                    'green' : 3
                }
                Response.objects.create(question=q, respondent=user, value=tl_dict[data], date_time=current_date_time, link_clicked=link_clicked)
            else: # text
                Response.objects.create(question=q, respondent=user, text=data, date_time=current_date_time, link_clicked=link_clicked)
        return redirect('/dashboard')
    else:
        return render(request, 'response.html', {'user' : user, 'task' : task, 'questions' : questions})

def get_responses(user, **kwargs):
    respondent = Respondent.objects.get(user=user)
    if kwargs.get('task') is not None:
        task = kwargs.get('task')
        questions = Question.objects.filter(task=task)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date_time')
    elif kwargs.get('question') is not None:
        question = kwargs.get('question')
        return Response.objects.filter(respondent=respondent, question=question).order_by('date_time')
    elif kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
        questions = Question.objects.filter(task__in=tasks)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date_time')
    else:
        return Response.objects.filter(respondent=respondent).order_by('date_time')

def calculate_score(values):
    """
    :param values: List of numbers from which you want to calculate a score.
    """
    values = list(filter(lambda value: value is not None, values))
    return 0 if not len(values) else sum(values) / len(values)

def task_is_completed(user, task):
    return bool(get_responses(user, task=task))