from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from allauth.account.views import SignupView
from .forms import GroupForm, TaskForm, QuestionFormset
from .models import *
from respondent.models import Respondent, Response, GroupRespondent
from respondent.views import calculate_score
from django.contrib.auth.decorators import login_required

import datetime
import operator
import matplotlib.pyplot as plt
from django.http import JsonResponse
import io
import base64
import urllib
from wordcloud import WordCloud
from PIL import Image

@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = get_object_or_404(Surveyor, user=request.user)
    return render(request, 'surveyor_dashboard.html', {'user' : user})

@login_required(login_url='/accounts/login/')
def leaderboard(request):
    user = get_object_or_404(Surveyor, user=request.user)
    return render(request, 'surveyor_leaderboard.html', {'user' : user})

@login_required(login_url='/accounts/login/')
def get_graphs_and_leaderboards_json(request):
    groups = get_groups(request.user).order_by('name')
    graphs = []
    leaderboards = []
    for group in groups:
        labels = get_graph_labels(request.user, group=group)
        scores = get_graph_data(request.user, labels, group=group)
        graphs.append({'title': group.name, 'labels': labels, 'scores': scores})
    
        leaderboards.append(get_leaderboard(request.user, group=group))
    
    return JsonResponse(data={
        'graphs': graphs,
        'leaderboards': leaderboards
    })

@login_required(login_url='/accounts/login/')
def task_overview(request, pk_task):
    user = get_object_or_404(Surveyor, user=request.user)
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

@login_required(login_url='/accounts/login/')
def new_task(request):
    user = get_object_or_404(Surveyor, user=request.user)
    group_surveyors = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
    groups = []

    for gr in group_surveyors:
        groups.append(Group.objects.get(pk=gr))

    if request.method == 'GET':
        form = TaskForm(request.GET or None)
        formset = QuestionFormset(queryset=Question.objects.none())
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        formset = QuestionFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.save()

            for question_form in formset:
                question = question_form.save(commit=False)
                question.task = task
                question.save()

            task.title = form.cleaned_data['title']
            task.due_date = form.cleaned_data['due_date']
            task.due_time = form.cleaned_data['due_time']
            task.group = Group.objects.get(name=form.cleaned_data['group'])
            return redirect('dashboard')
    else:
        form = NewTaskForm()

    return render(request, 'surveyor_new_task.html', {'user' : user, 'groups' : groups, 'taskform': form, 'formset': formset})

def get_groups(user):
    surveyor = Surveyor.objects.get(user=user)
    group_surveyors = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_surveyors) 
    return groups

def get_responses(user, **kwargs):
    surveyor = Surveyor.objects.get(user=user)
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
    else:
        groups = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group',flat=True)
        tasks = Task.objects.filter(group__in=groups)
    questions = Question.objects.filter(task__in=tasks)
    return Response.objects.filter(question__in=questions).order_by('date_time')

def get_graph_data(user, labels, **kwargs):
    responses = get_responses(user, **kwargs)

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
            if response.date_time.date() > date:
                break
            if response.date_time.date() > previous_date:
                queryset.append(response.value)
        scores.append(calculate_score(queryset) if queryset else previous_score)
        previous_date = date
        previous_score = scores[-1]
    
    assert(len(dates) == len(scores))
    return scores

def get_graph_labels(user, **kwargs):
    responses = get_responses(user, **kwargs)

    if not responses:
        return []

    num_intervals = min(len(responses), 10)
    dates = list(responses.values_list('date_time', flat=True))
    dates = [date_time.date() for date_time in dates]
    
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
    values = list(filter(lambda value: value is not None, values))
    return sum(values) / len(values)

def get_num_respondents_in_group(group):
    return GroupRespondent.objects.filter(group=group).count()

@login_required(login_url='/accounts/login/')
def get_tasks_json(request): # TODO: Remember to uncomment the tasks and comment out the temporary solution
    surveyor = Surveyor.objects.get(user=request.user)
    group_ids = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_ids)
    # today = datetime.datetime.now()
    # tasks = Task.objects.filter(group__in=groups).filter(due_date__gt=today.date()).filter(due_time__gt=today.time()).order_by('due_date', 'due_time')
    tasks = Task.objects.filter(group__in=groups).order_by('due_date', 'due_time')

    data = []
    for task in tasks:
        group = task.group # Might just return primary key rather than actual object
        questions = Question.objects.filter(task=task)
        responses = Response.objects.filter(question__in=questions)
        num_group_respondents = get_num_respondents_in_group(group)
        # Need to be able to tell complete responses - this is just a hack for now
        data.append({'pk': task.pk,
                     'title': task.title, 
                     'group_name': group.name, 
                     'num_respondents': num_group_respondents, 
                     'num_responses': responses.count() // questions.count(),
                     'due_date': task.due_date.strftime("%d/%m/%Y")})
    
    return JsonResponse(data={
        'rows': data
    })

@login_required(login_url='/accounts/login/')
def get_questions_json(request, pk_task):
    task = Task.objects.get(pk=pk_task)
    questions = Question.objects.filter(task=task)
    
    data = []
    for question in questions:
        link_clicks = 0
        responses = Response.objects.filter(question=question)
        pie_chart_labels = None
        pie_chart_data = None
        word_cloud = None

        if question.response_type == 1:
            response_type = "likert"
            pie_chart_labels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]
        elif question.response_type == 2:
            response_type = "traffic"
            pie_chart_labels = ['Red', 'Yellow', 'Green']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 4)]
        elif question.response_type == 3:
            response_type = "text"
        else:
            response_type = None
        
        if response_type == "text":
            word_cloud_dict = {}
            for response in responses:
                link_clicks += response.link_clicked
                word = response.text
                word_cloud_dict[word] = word_cloud_dict.get(word, 0) + 1
            word_cloud = create_word_cloud(word_cloud_dict)
        else:
            for response in responses:
                link_clicks += response.link_clicked
        
        data.append({
            'type': response_type,
            'description': question.description,
            'link_clicks': link_clicks,
            'pie_chart_labels': pie_chart_labels,
            'pie_chart_data': pie_chart_data,
            'word_cloud': word_cloud})
        
    return JsonResponse(data={
        'rows': data
    })

def create_word_cloud(word_cloud_dict):
    word_cloud = WordCloud(background_color=None, mode="RGBA").generate_from_frequencies(word_cloud_dict)
    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64
        
@login_required(login_url='/accounts/login/')
def get_leaderboard_json(request):
    group_param = request.GET.get('group', None)
    if group_param is not None:
        group = Group.objects.get(pk=group_param)
        return JsonResponse(data={
            'rows': get_leaderboard(request.user, group=group)
        })
    else:
        return JsonResponse(data={
            'rows': get_leaderboard(request.user)
        })

@login_required(login_url='/accounts/login/')
def get_leaderboard_groups_json(request):
    groups = get_groups(request.user)
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

def get_leaderboard(user, **kwargs):
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        groups = get_groups(user)
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

@login_required(login_url='/accounts/login/')
def new_group(request):
    data = dict()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            GroupSurveyor.objects.create(group=group, surveyor=Surveyor.objects.get(user=request.user))
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = GroupForm()

    context = {'form': form}
    data['html_form'] = render_to_string('partial_new_group.html',
        context,
        request=request
    )
    return JsonResponse(data)
