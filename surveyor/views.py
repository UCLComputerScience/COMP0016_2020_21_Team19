from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from tablib import Dataset

from .handler import *
from surveyor.utils import *
from .forms import *


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    The Dashboard page for the ``Surveyor``.
    Displays each incomplete ``Task`` they have set, as well as an overview of the leaderboard and progress of each ``Group``.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/dashboard.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        tasks = get_tasks_data(user)
        tasks = [task for task in tasks if not task.completed]
        group_data = get_graphs_and_leaderboards(user)
        return render(request, 'surveyor/dashboard.html',
                    {'user': user, 'tasks': tasks, 'now': datetime.datetime.now(), 'group_data': group_data})


@login_required(login_url='/accounts/login/')
def leaderboard(request):
    """
    The Leaderboard page for the ``Surveyor``.
    Displays rankings for the ``Respondent``\s in each `Group`.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/leaderboard.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        groups = get_groups(user)
        for group in groups:
            group.leaderboard = get_leaderboard(user, group=group)
        return render(request, 'surveyor/leaderboard.html',
                    {'user': user, 'groups': groups, 'overall_leaderboard': get_leaderboard(user)})


@login_required(login_url='/accounts/login/')
def history(request):
    """
    The Task History page for the ``Surveyor``.
    Displays all of the previous tasks that the ``Surveyor`` has set.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/history.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        tasks = get_tasks_data(user)
        return render(request, 'surveyor/history.html', {'user': user, 'tasks': tasks})


@login_required(login_url='/accounts/login/')
def organisation(request):
    """
    The Organisation page for the ``Surveyor``.
    Displays the ``Surveyor``\s present in the ``Organisation`` and allows invitations
    for new ``Surveyor``\s.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/organisation.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Surveyor, user=request.user)

    if request.method == 'GET':
        surveyors = Surveyor.objects.filter(organisation=user.organisation)
        form_inv = InviteSurveyorForm()
        import_form = MultipleUserForm()
        return render(request, 'surveyor/organisation.html',
                    {'user': user, 'surveyors': surveyors, 'organisation': user.organisation, 'form_inv': form_inv,
                    'import_form': import_form})
    elif request.method == 'POST':
        return post_organisation(request, user)


@login_required(login_url='/accounts/login/')
def users(request):
    """
    Displays a list of all the ``Respondent``\s which the ``Surveyor`` manages.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/users.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        groups = get_groups(user)
        respondents = get_respondents_by_groups(groups)
        respondents = set_respondent_groups(respondents, groups)

        return render(request, 'surveyor/users.html', {'user': user, 'respondents': respondents})


@login_required(login_url='/accounts/login/')
def user_progress(request, user_id):
    """
    The user progress page for an individual ``Respondent``.
    Displays all of the previous tasks set by the current ``Surveyor`` which the ``Respondent`` has responded to, the progress that they've shown and their individual responses to these tasks.

    :param request: ``GET`` request made by the current user.
    :type request: django.http.HttpRequest
    :param user_id: Primary key of the ``Respondent`` for which to show data.
    :type user_id: uuid.UUID
    :return: The ``surveyor/user-progress.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        respondent = Respondent.objects.get(id=user_id)
        groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
        tasks = get_tasks_data(user).filter(group__in=groups)
        
        tasks = [task for task in tasks if has_responded_to_task(respondent, task)]

        neutral_word_cloud = get_word_cloud(user, respondent)
        positive_word_cloud = get_word_cloud(user,respondent, text_positive=True)
        negative_word_cloud = get_word_cloud(user, respondent, text_positive=False)
        graphs = [graph for graph in get_progress_graphs(respondent) if graph['id'] in groups]
        
        for graph in graphs:
            del graph['id'] # Remove to fit Chart.js expected format
            
        return render(request, 'surveyor/user-progress.html',
                     {'user': user, 'respondent': respondent, 'tasks': tasks, 'graphs': graphs,
                      'neutral_word_cloud': neutral_word_cloud, 'positive_word_cloud': positive_word_cloud,
                      'negative_word_cloud': negative_word_cloud})


@login_required(login_url='/accounts/login/')
def user_response(request, user_id, task_id):
    """
    The page showing the ``Response`` of a ``Respondent`` to a given ``Task``.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :param user_id: The primary key of the ``Respondent``.
    :type user_id: uuid.UUID
    :param task_id: The primary key of the ``Task``.
    :type task_id: uuid.UUID
    :return: The ``surveyor/user-response.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        respondent = Respondent.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)
        questions = Question.objects.filter(task=task)
        responses = Response.objects.filter(question__in=questions, respondent=respondent)
        for question in questions:
            question.response = responses.get(question=question)
        return render(request, 'surveyor/user-response.html',
                    {'user': user, 'respondent': respondent, 'task': task, 'questions': questions,
                    'responses': responses})


@login_required(login_url='/accounts/login/')
def task_overview(request, task_id):
    """
    Summary page containing the collective responses of the group which has been assigned a ``Task``.
    Categorical responses are visualised using either Bar or Pie charts and textual responses are visualised in word clouds.

    :param request: ``GET`` request made by the current ``Surveyor``.
    :type request: django.http.HttpRequest
    :param task_id: The ``UUID`` primary key of the ``Task`` object being queried for a summary of responses.
    :type task_id: uuid.UUID
    :return: The ``surveyor/task-overview.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        task = get_object_or_404(Task, id=task_id)
        questions = Question.objects.filter(task=task)
        num_responses = Response.objects.filter(question__in=questions).count()

        data = {
            'user': user,
            'task': task,
            'task_total_respondents': get_num_respondents_in_group(task.group),
            'task_respondents_completed': num_responses // questions.count(),
            'summary': get_task_summary(task_id)
        }

        return render(request, 'surveyor/task-overview.html', data)
    
    elif request.method == 'POST':
        return post_task_overview(request)


@login_required(login_url='/accounts/login/')
def new_task(request):
    """
    The page containing the form for creating a new ``Task``.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/new-task.html`` template rendered using the given dictionary or a HttpResponseRedirect to the dashboard.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Surveyor, user=request.user)

    if request.method == 'GET':
        groups = get_groups(user)
        return render(request, 'surveyor/new-task.html', get_new_task(groups, request, user))
    elif request.method == 'POST':
        return post_new_task(request, user)


@login_required(login_url='/accounts/login/')
def groups(request):
    """
    Displays a list of all the ``Group``\s which the ``Surveyor`` manages.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/groups.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        groups = get_groups(user)
        for group in groups:
            group.num_participants = get_num_respondents_in_group(group)
        form = GroupForm()
        return render(request, 'surveyor/groups.html', {'user': user, 'groups': groups, 'form': form})
    elif request.method == 'POST':
        return post_groups(request)
        


@login_required(login_url='/accounts/login/')
def manage_group(request, group_id):
    """
    The page allowing for the management (addition/deletion) of ``Respondent``\s in a group.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :param group_id: Primary key of the ``Group`` object stored in the database.
    :type group_id: uuid.UUID
    :return: The ``surveyor/manage-group.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'GET':
        user = get_object_or_404(Surveyor, user=request.user)
        group = Group.objects.get(id=group_id)
        respondents = get_group_participants(group)
        form = AddUserForm(group_id=group_id)
        form_inv = InviteUserForm()
        import_form = MultipleUserForm()
        return render(request, 'surveyor/manage-group.html',
                    {'user': user, 'participants': respondents, 'group': group, 'form': form, 'form_inv': form_inv,
                    'import_form': import_form})
    elif request.method == 'POST':
        return post_manage_group(request, group_id)
        
