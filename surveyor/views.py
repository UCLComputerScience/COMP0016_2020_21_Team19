from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from .forms import GroupForm, TaskForm, QuestionFormset, AddUserForm, InviteUserForm
from .models import *
from respondent.models import Respondent, Response, GroupRespondent
from respondent.views import calculate_score
from django.contrib.auth.decorators import login_required
from django import forms
from core.utils import *
from surveyor.utils import *
from core.models import UserInvitation

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
    user = get_object_or_404(Surveyor, user=request.user)
    tasks, now = get_tasks(user)
    tasks = [task for task in tasks if not task.completed]
    group_data = get_graphs_and_leaderboards(user)
    return render(request, 'surveyor/dashboard.html', {'user' : user, 'tasks': tasks, 'now':now, 'group_data': group_data})

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
    user = get_object_or_404(Surveyor, user=request.user)
    groups = get_groups(user)
    for group in groups:
        group.leaderboard = get_leaderboard(user, group=group)
    return render(request, 'surveyor/leaderboard.html', {'user' : user, 'groups': groups, 'overall_leaderboard': get_leaderboard(user)})

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
    user = get_object_or_404(Surveyor, user=request.user)
    tasks, now = get_tasks(user)
    return render(request, 'surveyor/history.html', {'user': user, 'tasks': tasks})

@login_required(login_url='/accounts/login/')
def users(request):
    """
    Displays a list of all the ``Respondent``\s which the ``Surveyor`` manages.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/users.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    user = get_object_or_404(Surveyor, user=request.user)
    groups = get_groups(user)
    colors = ["primary", "secondary", "danger", "warning", "info", "light", "dark"]
    group_colors = {group.id: random.choice(colors) for group in groups}

    respondents = Respondent.objects.none()
    for group in groups:
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
        respondents |= Respondent.objects.filter(id__in=respondent_ids)

    for respondent in respondents:
        group_ids = GroupRespondent.objects.filter(respondent=respondent).values_list('group', flat=True)
        respondent.groups = groups.filter(id__in=group_ids)
        for group in respondent.groups:
            group.color = group_colors[group.id]
            
    return render(request, 'surveyor/users.html', {'user': user, 'respondents': respondents})

@login_required(login_url='/accounts/login/')
def user_progress(request, pk_user):
    """
    The user progress page for an individual ``Respondent``.
    Displays all of the previous tasks set by the current ``Surveyor`` which the ``Respondent`` has responded to, the progress that they've shown and their individual responses to these tasks.

    :param request: ``GET`` request made by the current user.
    :type request: django.http.HttpRequest
    :param pk_user: Primary key of the ``Surveyor`` accessing the page.
    :type pk_user: uuid.UUID
    :return: The ``surveyor/user_progress.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
    user = get_object_or_404(Surveyor, user=request.user)
    respondent = Respondent.objects.get(pk=pk_user)
    tasks, now = get_tasks(user)
    groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
    tasks = tasks.filter(group__in=groups)
    new_tasks = []
    for task in tasks:
        if has_responded_to_task(respondent, task):
            new_tasks.append(task)
    word_cloud = get_overall_word_cloud(user, respondent)
    graphs = [graph for graph in get_progress_graphs(respondent) if graph['id'] in groups]
    for graph in graphs:
        del graph['id']
    return render(request, 'surveyor/user_progress.html', {'user': user, 'respondent': respondent, 'tasks': new_tasks, 'graphs': graphs, 'overall_word_cloud': word_cloud})

@login_required(login_url='/accounts/login/')
def user_response(request, pk_user, pk_task):
    """
    The page showing the ``Response`` of a ``Respondent`` to a given ``Task``.

    :param request: The ``GET`` request made by the user.
    :type request: django.http.HttpRequest
    :param pk_user: The primary key of the ``Respondent``.
    :type pk_user: uuid.UUID
    :param pk_task: The primary key of the ``Task``.
    :type pk_task: uuid.UUID
    :return: The ``surveyor/user_response.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
    user = get_object_or_404(Surveyor, user=request.user)
    respondent = Respondent.objects.get(pk=pk_user)
    task = Task.objects.get(pk=pk_task)
    questions = Question.objects.filter(task=task)
    responses = Response.objects.filter(question__in=questions, respondent=respondent)
    for question in questions:
        question.response = responses.get(question=question)
    return render(request, 'surveyor/user_response.html', {'respondent': respondent, 'task': task, 'questions': questions, 'responses': responses})

@login_required(login_url='/accounts/login/')
def task_overview(request, pk_task):
    """
    Summary page containing the collective responses of the group which has been assigned a ``Task``.
    Categorical responses are visualised using either Bar or Pie charts and textual responses are visualised in word clouds.

    :param request: ``GET`` request made by the current ``Surveyor``.
    :type request: django.http.HttpRequest
    :param pk_task: The ``UUID`` primary key of the ``Task`` object being queried for a summary of responses.
    :type pk_task: uuid.UUID
    :return: The ``surveyor/task_overview.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """
    if request.method == 'POST':
        if request.POST.get('task_status') == 'complete':
            task_pk = request.POST.get('task')
            task = Task.objects.get(pk=task_pk)
            task.completed = True
            task.save()
        if request.POST.get('task_status') == 'incomplete':
            task_pk = request.POST.get('task')
            task = Task.objects.get(pk=task_pk)
            task.completed = False
            task.save()
    
    user = get_object_or_404(Surveyor, user=request.user)
    task = get_object_or_404(Task, pk=pk_task)
    questions = Question.objects.filter(task=task)
    num_responses = Response.objects.filter(question__in=questions).count()

    data = {
        'user': user,
        'task': task,
        'task_total_respondents': get_num_respondents_in_group(task.group),
        'task_respondents_completed': num_responses // questions.count(),
        'questions': get_questions(pk_task),
    }
    return render(request, 'surveyor/task_overview.html', data)

@login_required(login_url='/accounts/login/')
def new_task(request):
    """
    The page containing the form for creating a new ``Task``.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/new_task.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
    user = get_object_or_404(Surveyor, user=request.user)
    group_surveyors = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
    groups = []

    for gr in group_surveyors:
        groups.append(Group.objects.get(pk=gr))

    if request.method == 'GET':
        form = TaskForm(request.GET or None, request=request)
        formset = QuestionFormset(queryset=Question.objects.none())
    elif request.method == 'POST':
        form = TaskForm(request.POST, request=None)
        formset = QuestionFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.save()

            for question_form in formset:
                link = question_form.cleaned_data['link']
                question_form.cleaned_data['link'] = sanitize_link(link)
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

    return render(request, 'surveyor/new_task.html', {'user' : user, 'groups' : groups, 'taskform': form, 'formset': formset})


@login_required(login_url='/accounts/login/')
def new_group(request):
    """
    Modal popup containing a form for the creation of a new ``Group``.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/partials/new_group.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
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
    data['html_form'] = render_to_string('surveyor/partials/new_group.html',
        context,
        request=request
    )
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def groups(request):
    """
    Displays a list of all the ``Group``\s which the ``Surveyor`` manages.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :return: The ``surveyor/groups.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
    user = get_object_or_404(Surveyor, user=request.user)
    if request.method == 'POST':
        if request.POST.get('request_type') == 'delete_group':
            group_pk = request.POST.get('group')
            group = Group.objects.filter(pk=group_pk).delete()

    groups = get_groups(user)
    for group in groups:
        group.num_participants = get_num_respondents_in_group(group)        
    return render(request, 'surveyor/groups.html', {'user': user, 'groups': groups})

@login_required(login_url='/accounts/login/')
def manage_group(request, pk_group):
    """
    The page allowing for the management (addition/deletion) of ``Respondent``\s in a group.

    :param request: The ``GET``/``POST`` request made by the user.
    :type request: django.http.HttpRequest
    :param pk_group: Primary key of the ``Group`` object stored in the database.
    :type pk_group: uuid.UUID
    :return: The ``surveyor/manage_group.html`` template rendered using the given dictionary.
    :rtype: django.http.HttpResponse
    """    
    if request.method == 'POST':
        group = Group.objects.get(pk=pk_group)
        if request.POST.get('request_type') == 'delete_participant': # Deleting a participant
            respondent_pk = request.POST.get('respondent')
            respondent = Respondent.objects.get(pk=respondent_pk)
            GroupRespondent.objects.filter(respondent=respondent, group=group).delete()
        elif request.POST.get('request_type') == 'invite': # Inviting a participant
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                respondent = Respondent.objects.get(user=user)
                GroupRespondent.objects.create(
                    group=group, 
                    respondent=respondent
                )
            else:
                invite = UserInvitation.create(
                    email,
                    inviter=request.user,
                    group=group,
                    is_respondent=True
                )
                invite.send_invitation(request)
        else: # Adding a participant
            respondent_pk = request.POST.get('respondent')
            respondent = Respondent.objects.get(pk=respondent_pk)
            new_object = GroupRespondent.objects.create(group=group, respondent=respondent)

    user = get_object_or_404(Surveyor, user=request.user)
    group = Group.objects.get(pk=pk_group)
    respondents = get_group_participants(group)
    form = AddUserForm(group_pk=pk_group)
    form_inv = InviteUserForm()
    return render(request, 'surveyor/manage_group.html', {'user': user, 'participants': respondents, 'group': group, 'form': form, 'form_inv': form_inv})