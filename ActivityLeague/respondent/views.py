from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from surveyor.models import *
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from core.utils import *

import random

@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = get_object_or_404(Respondent, user=request.user)
    tasks, now = get_tasks(user)
    return render(request, 'respondent_dashboard.html', {'user' : user, 'tasks' : tasks, 'now' : now})

@login_required(login_url='/accounts/login/')
def leaderboard(request):
    user = get_object_or_404(Respondent, user=request.user)
    return render(request, 'respondent_leaderboard.html', {'user' : user})

@login_required(login_url='/accounts/login/')
def progress(request):
    user = get_object_or_404(Respondent, user=request.user)
    labels = get_graph_labels(user)
    scores = get_graph_data(user, labels)
    groups = get_groups(user)
    return render(request, 'respondent_progress_page.html', {'user' : user, 'labels': labels, 'scores': scores, 'groups': groups})

@login_required(login_url='/accounts/login/')
def get_progress_json(request):
    user = get_object_or_404(Respondent, user=request.user)
    groups = get_groups(user)
    overall_labels = get_graph_labels(user)

    group_graphs = []
    overall_data = []
    for group in groups:
        group_labels = get_graph_labels(user, group=group)
        group_scores = get_graph_data(user, group_labels, group=group)
        group_title = group.name
        group_graphs.append({ 'title': group_title, 'labels': group_labels, 'scores': [get_chartjs_dict(group_scores)] })

        overall_data.append(get_chartjs_dict(group_scores))

    return JsonResponse(data={
        'overall': overall_data,
        'overall_labels': overall_labels,
        'groups': group_graphs
    })

@login_required(login_url='/accounts/login/')
def response(request, id):
    user = get_object_or_404(Respondent, user=request.user)
    task = Task.objects.get(id=id)
    questions = Question.objects.filter(task=task)
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