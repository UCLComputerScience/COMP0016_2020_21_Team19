from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import GroupForm, TaskForm, QuestionFormset
from .models import *
from respondent.models import Respondent, Response, GroupRespondent
from respondent.views import calculate_score

import datetime
import operator
from django.http import JsonResponse

def get_graphs_and_leaderboards_json(request, pk):
    groups = get_groups(pk).order_by('name')
    graphs = []
    leaderboards = []
    for group in groups:
        labels = get_graph_labels(pk, group=group)
        scores = get_graph_data(pk, labels, group=group)
        graphs.append({'title': group.name, 'labels': labels, 'scores': scores})
    
        leaderboards.append(get_leaderboard(pk, group=group))
    
    return JsonResponse(data={
        'graphs': graphs,
        'leaderboards': leaderboards
    })

def dashboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_dashboard.html', {'user' : user, 'pk':pk})

def leaderboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_leaderboard.html', {'user' : user, 'pk': pk})

def task_overview(request, pk, pk_task):
    user = get_object_or_404(Surveyor, pk=pk)
    task = get_object_or_404(Task, pk=pk_task)
    questions = Question.objects.filter(task=task)
    num_responses = Response.objects.filter(question__in=questions).count()
    data = {
        'user': user,
        'task_pk': pk_task,
        'task_title': task.title,
        'task_total_students': get_num_respondents_in_group(task.group),
        'task_students_completed': num_responses // questions.count(),
        'task_due_date': task.due_date.strftime("%d/%m/%Y")
    }
    return render(request, 'task_overview.html', data)

def new_task(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    group_surveyors = GroupSurveyor.objects.filter(surveyor=user)
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

def get_groups(pk):
    surveyor = Surveyor.objects.get(pk=pk)
    group_ids = GroupSurveyor.objects.filter(surveyor=surveyor)
    return Group.objects.filter(pk__in=group_ids)

def get_responses(pk, **kwargs):
    surveyor = Surveyor.objects.get(pk=pk)
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
    else:
        groups = GroupSurveyor.objects.filter(surveyor=surveyor).values_list(flat=True)
        tasks = Task.objects.filter(group__in=groups)
    questions = Question.objects.filter(task__in=tasks)
    return Response.objects.filter(question__in=questions).order_by('date', 'time')

def get_graph_data(pk, labels, **kwargs):
    responses = get_responses(pk, **kwargs)

    if not responses:
        return []

    dates = [datetime.datetime.strptime(label, '%Y-%m-%d').date() for label in labels]

    if len(dates) == 0:
        return None
    elif len(dates) == 1:
        return responses[0].value

    scores = []
    previous_date = datetime.date.min
    previous_score = 0
    for date in dates:
        queryset = []
        for response in responses:
            if response.date > date:
                break
            if response.date > previous_date:
                queryset.append(response.value)
        scores.append(calculate_score(queryset) if queryset else previous_score)
        previous_date = date
        previous_score = scores[-1]
    
    assert(len(dates) == len(scores))
    return scores

def get_graph_labels(pk, **kwargs):
    responses = get_responses(pk, **kwargs)

    if not responses:
        return []

    num_intervals = min(len(responses), 10)
    dates = list(responses.values_list('date', flat=True))
    
    if len(responses) == 0:
        return None
    elif len(dates) == 1:
        return dates
    
    latest = dates[-1]
    earliest = dates[0]
    time_range = latest - earliest

    interval = time_range / num_intervals

    labels = [str(earliest + (interval * i)) for i in range(num_intervals + 1)]
    
    return labels

def calculate_score(values):
    """
    :param responses: List of numbers from which you want to calculate a score.
    """
    return sum(values) / len(values)

def get_num_respondents_in_group(group):
    return GroupRespondent.objects.filter(group=group).count()

def get_tasks_json(request, pk): # TODO: Remember to uncomment the tasks and comment out the temporary solution
    surveyor = Surveyor.objects.get(pk=pk)
    group_ids = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_ids)
    # today = datetime.datetime.now()
    # tasks = Task.objects.filter(group__in=groups).filter(due_date__gt=today.date()).filter(due_time__gt=today.time()).order_by('due_date', 'due_time')
    tasks = Task.objects.filter(group__in=groups).order_by('due_date', 'due_time')

    data = []
    for task in tasks:
        group = task.group # Might just return primary key rather than actual object
        questions = Question.objects.filter(task=task)
        num_responses = Response.objects.filter(question__in=questions).count()
        num_group_respondents = get_num_respondents_in_group(group)
        # Need to be able to tell complete responses - this is just a hack for now
        data.append({'pk': task.pk,
                     'title': task.title, 
                     'group_name': group.name, 
                     'num_respondents': num_group_respondents, 
                     'num_responses': num_responses // questions.count(),
                     'due_date': task.due_date.strftime("%d/%m/%Y")})
    
    return JsonResponse(data={
        'rows': data
    })

def get_questions_json(request, pk, pk_task):
    task = Task.objects.get(pk=pk_task)
    questions = Question.objects.filter(task=task)
    
    data = []
    for question in questions:
        link_clicks = 0
        responses = Response.objects.filter(question=question)
        pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]
        data.append({
            'description': question.description,
            'link_clicks': link_clicks,
            'pie_chart_labels': ['1', '2', '3', '4', '5'],
            'pie_chart_data': pie_chart_data})
        
    return JsonResponse(data={
        'rows': data
    })
        
def get_leaderboard_json(request, pk):
    group_param = request.GET.get('group', None)
    if group_param is not None:
        group = Group.objects.get(pk=group_param)
        return JsonResponse(data={
            'rows': get_leaderboard(pk, group=group)
        })
    else:
        return JsonResponse(data={
            'rows': get_leaderboard(pk)
        })

def get_leaderboard_groups_json(request, pk):
    groups = get_groups(pk)
    data = []
    for group in groups:
        entry = {
            'name': group.name,
            'group_key': str(group.id)
        }
        data.append(entry)
    
    return JsonResponse(data={
        'buttons': data
    })

def get_leaderboard(pk, **kwargs):
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        groups = get_groups(pk)
        respondent_ids = GroupRespondent.objects.filter(group__in=groups).values_list('respondent', flat=True)
    respondents = Respondent.objects.filter(pk__in=respondent_ids)
    
    score_list = []
    for respondent in respondents:
        # Get their responses and calculate their score
        responses = Response.objects.filter(respondent=respondent).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': score}
        score_list.append(entry)
        
    score_list.sort(key=operator.itemgetter('score'), reverse=True)

    return score_list

def new_group(request, pk):
    data = dict()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            GroupSurveyor.objects.create(group=group, surveyor=Surveyor.objects.get(id=pk))
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = GroupForm()

    context = {'form': form, 'pk' : pk}
    data['html_form'] = render_to_string('partial_new_group.html',
        context,
        request=request
    )
    return JsonResponse(data)
