from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm, QuestionFormset
from .models import *
from respondent.models import Respondent, Response, GroupRespondent
from respondent.views import calculate_score

import datetime
import operator
from django.http import JsonResponse


def dashboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_dashboard.html', {'user' : user, 'pk':pk})
    # return render(request, 'surveyor_dashboard.html')

def leaderboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_leaderboard.html', {'user' : user, 'pk': pk})
    # return render(request, 'surveyor_leaderboard.html')

def task_overview(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'task_overview.html', {'user' : user})
    # return render(request, 'task_overview.html')

def new_task(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    group_surveyors = GroupSurveyor.objects.filter(surveyor_id=pk)
    groups = []

    for gr in group_surveyors:
        groups.append(Group.objects.get(pk=gr.id))

    if request.method == 'GET':
        form = TaskForm(request.GET or None)
        formset = QuestionFormset(queryset=Question.objects.none())
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        formset = QuestionFormset(request.POST)
        # if form.is_valid() and formset.is_valid():
        print("Valid form" if form.is_valid() else "Invalid form")
        print(form.errors)
        if True:
            task = form.save(commit=False)
            task.save()

            for question_form in formset:
                question = question_form.save(commit=False)
                question.task = task
                
                # TODO: Add the other question fields
                question.save() # BUG

            task.title = form.cleaned_data['title']
            task.due_date = form.cleaned_data['due_date']
            task.due_time = form.cleaned_data['due_time']
            task.group = Group.objects.get(name=form.cleaned_data['group'])
            print(task.title)
            # task.save()
            # task = Task.objects.create(
            #     title=form.cleaned_data.get('message'),
            #     topic=topic,
            #     created_by=user
            # )
            return redirect('surveyor_dashboard', pk=user.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTaskForm()

    return render(request, 'surveyor_new_task.html', {'user' : user, 'groups' : groups, 'taskform': form, 'formset': formset})
    # return render(request, 'surveyor_new_task.html')

def get_surveyor_progress_labels(pk, **kwargs):

    if kwargs.get('group') is not None:
        pass

    surveyor = Surveyor.objects.get(pk=pk)
    groups = GroupSurveyor.objects.filter(surveyor=surveyor).values_list(flat=True)
    tasks = Task.objects.filter(group__in=groups)
    questions = Question.objects.filter(task__in=tasks)
    repsonses = Response.objects.filter(question__in=questions)

    # TODO: This method is incomplete

def get_num_respondents_in_group(group):
    return GroupRespondent.objects.filter(group=group).count()

def get_tasks_json(request, pk): # TODO: Remember to uncomment the tasks and comment out the temporary solution
    surveyor = Surveyor.objects.get(pk=pk)
    group_ids = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_ids)
    today = datetime.datetime.now()
    # tasks = Task.objects.filter(group__in=groups).filter(due_date__gt=today.date()).filter(due_time__gt=today.time()).order_by('due_date', 'due_time')
    tasks = Task.objects.filter(group__in=groups).order_by('due_date', 'due_time')

    data = []
    for task in tasks:
        group = task.group # Might just return primary key rather than actual object
        questions = Question.objects.filter(task=task)
        num_responses = Response.objects.filter(question__in=questions).count()
        num_group_respondents = get_num_respondents_in_group(group)
        # Need to be able to tell complete responses - this is just a hack for now
        entry = {'title': task.title, 
                 'group_name': group.name, 
                 'num_respondents': num_group_respondents, 
                 'num_responses': num_responses // (questions.count() * num_group_respondents),
                 'due_date': task.due_date}
        data.append(entry)
    
    return JsonResponse(data={
        'rows': data
    })

def get_leaderboard_json(request, pk):
    # Leaderboard is overall: ranked on highest average reported score
    surveyor = Surveyor.objects.get(pk=pk)
    group_ids = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_ids)
    respondent_ids = GroupRespondent.objects.filter(group__in=groups).values_list('respondent', flat=True)
    respondents = Respondent.objects.filter(pk__in=respondent_ids)
    
    score_list = []
    for respondent in respondents:
        # Get their responses and calculate their score
        responses = Response.objects.filter(respondent=respondent).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': score}
        score_list.append(entry)
        
    score_list.sort(key=operator.itemgetter('score'))

    return JsonResponse(data={
        'rows': score_list
    })

    
