import datetime
import operator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from surveyor.models import *

# Create your views here.
def dashboard(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
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

def leaderboard(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    respondents = Respondent.objects.all()
    return render(request, 'respondent_leaderboard.html', {'user' : user, 'respondents' : respondents, 'pk': pk})
    # return render(request, 'respondent_leaderboard.html')

def progress(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    labels = get_progress_labels(pk)
    scores = get_progress_values(pk, labels)
    groups = get_groups(pk)
    return render(request, 'respondent_progress_page.html', {'pk': pk, 'user' : user, 'labels': labels, 'scores': scores, 'groups': groups})

def get_progress_json(request, pk):
    groups = get_groups(pk)
    overall_labels = get_progress_labels(pk)

    overall_progress = { 'labels': overall_labels, 'scores': get_progress_values(pk, overall_labels) }
    group_graphs = []
    for group in groups:
        group_labels = get_progress_labels(pk, group=group)
        group_scores = get_progress_values(pk, group_labels, group=group)
        group_title = group.name
        group_graphs.append({ 'title': group_title, 'labels': group_labels, 'scores': group_scores })

    return JsonResponse(data={
        'overall': overall_progress,
        'groups': group_graphs
    })
    
def response(request, pk, id):
    user = get_object_or_404(Respondent, pk=pk)
    task = Task.objects.get(id=id)
    questions = Question.objects.filter(task=task)
    return render(request, 'response.html', {'user' : user, 'task' : task, 'questions' : questions})

def login(request):
    return render(request, 'login.html')

def get_responses(pk, **kwargs):
    respondent = Respondent.objects.get(pk=pk)
    if kwargs.get('task') is not None:
        task = kwargs.get('task')
        questions = Question.objects.filter(task=task)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date', 'time')
    elif kwargs.get('question') is not None:
        question = kwargs.get('question')
        return Response.objects.filter(respondent=respondent, question=question).order_by('date', 'time')
    elif kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
        questions = Question.objects.filter(task__in=tasks)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date', 'time')
    else:
        return Response.objects.filter(respondent=respondent).order_by('date', 'time')

def get_progress_values(pk, labels,  **kwargs):
    """
    Retrieves the values to be plotted by Chart.js on respondent_progress_page.html.

    Args:
        pk (int): Primary key of the respondent whose progress we are to be 
                  displaying.
        labels (list: string): List of string datetimes that are the labels
                               on the x-axis of the graph that to be displayed.
        **kwargs: Expects group of type Group. This is passed, this methiod 
                  shall return the progress values for the labels for the
                  group that is passed.

    Returns:
        (list:num): List of values of length labels.length corresponding to the
                    values to be plotted.
    """
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


# TODO: Rewrite this method to consider the text values.
def get_progress_labels(pk, **kwargs):
    """
    Retrieves labels for chart.js on respondent_progress_page.html based on
    the existing respondent's responses.
    
    Args:
        pk (int): Primary key of the respondent for which we are rendering a chart.

    Returns:
        list: 
    """
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

def get_respondent_leaderboard_json(request, pk):
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

def get_respondent_leaderboard_groups_json(request, pk):
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
    respondent = Respondent.objects.get(pk=pk)

    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        current_groups = GroupRespondent.objects.filter(respondent=respondent).values_list('group', flat=True)
        respondent_ids = GroupRespondent.objects.filter(group__in=current_groups).values_list('respondent', flat=True)
    
    respondents = Respondent.objects.filter(pk__in=respondent_ids)
    
    rows = []
    for respondent in respondents:
        responses = Response.objects.filter(respondent=respondent).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': score}
        rows.append(entry)
    
    rows.sort(key=operator.itemgetter('score'), reverse=True)

    return rows

def get_groups(pk):
    respondent = Respondent.objects.get(pk=pk)
    group_ids = GroupRespondent.objects.filter(respondent=respondent).values_list('group', flat=True)
    groups = Group.objects.filter(pk__in=group_ids)
    return groups