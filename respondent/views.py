from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .handler import *
from core.utils import *
from core.models import Question


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    Returns the Dashboard page for a ``Respondent``.
    Displays each incomplete ``Task`` that they have been set.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``respondent/dashboard.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Respondent, user=request.user)
    tasks = get_tasks_data(user)
    return render(request, 'respondent/dashboard.html', {'user': user, 'tasks': tasks, 'now': datetime.datetime.now()})


@login_required(login_url='/accounts/login/')
def leaderboard(request):
    """
    The Leaderboard page for the ``Respondent``.
    Displays the leaderboard for each ``Group`` the ``Respondent`` is a member of.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``respondent/leaderboard.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Respondent, user=request.user)
    groups = get_groups(user)
    for group in groups:
        group.leaderboard = get_leaderboard(user, group=group)
    return render(request, 'respondent/leaderboard.html',
                  {'user': user, 'groups': groups, 'overall_leaderboard': get_leaderboard(user)})


@login_required(login_url='/accounts/login/')
def progress(request):
    """
    The Progress page for the ``Respondent``.
    Displays the progress graphs for each ``Group`` that the ``Respondent`` is in.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``respondent/progress.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Respondent, user=request.user)
    group_graphs = get_progress_graphs(user)
    return render(request, 'respondent/progress.html', {'user': user, 'group_graphs': group_graphs})


@login_required(login_url='/accounts/login/')
def response(request, id):
    """
    The page containing the form for submitting the ``Response``\s to a ``Task``.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :param id: The primary key of the ``Task``.
    :type id: uuid.UUID
    :return: If ``request.method == GET`` request, this returns the ``respondent/response.html`` template rendered with the given dictionary.
             Otherwise, this returns a redirect to the dashboard.
    :rtype: django.http.HttpResponse / django.http.HttpResponseRedirect
    """
    user = get_object_or_404(Respondent, user=request.user)
    task = Task.objects.get(id=id)
    questions = Question.objects.filter(task=task)

    if request.method == 'POST':
        post_response(request, user)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'respondent/response.html', {'user': user, 'task': task, 'questions': questions})
