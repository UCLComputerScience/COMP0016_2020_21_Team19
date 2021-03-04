from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from core.utils import *


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
    tasks, now = get_tasks(user)
    return render(request, 'respondent/dashboard.html', {'user': user, 'tasks': tasks, 'now': now})


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
    return render(request, 'respondent/progress.html', {'user': user, 'groups': group_graphs})


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
            if q.response_type == 1:  # likert
                likert_dict = {
                    'strong_disagree': 1,
                    'disagree': 2,
                    'neutral': 3,
                    'agree': 4,
                    'strong_agree': 5
                }
                Response.objects.create(question=q, respondent=user, value=likert_dict[data],
                                        date_time=current_date_time, link_clicked=link_clicked)
            elif q.response_type == 2:  # traffic light
                tl_dict = {
                    'red': 1,
                    'yellow': 2,
                    'green': 3
                }
                Response.objects.create(question=q, respondent=user, value=tl_dict[data], date_time=current_date_time,
                                        link_clicked=link_clicked)
            elif q.response_type == 4:  # Numerical Radio Buttons
                Response.objects.create(question=q, respondent=user, value=int(data), date_time=current_date_time,
                                        link_clicked=link_clicked)
            elif q.response_type == 3:  # Text
                Response.objects.create(question=q, respondent=user, text=data, date_time=current_date_time,
                                        link_clicked=link_clicked)
            elif q.response_type == 5:  # Text (Positive)
                Response.objects.create(question=q, respondent=user, text=data, date_time=current_date_time,
                                        link_clicked=link_clicked, text_positive=True)
            else:  # == 6 | Text (Negative)
                Response.objects.create(question=q, respondent=user, text=data, date_time=current_date_time,
                                        link_clicked=link_clicked, text_positive=False)

            # mark completed if all respondents have completed the task
            group = q.task.group
            questions = Question.objects.filter(task=q.task)
            num_responses = Response.objects.filter(question__in=questions).count()
            if num_responses == get_num_respondents_in_group(group):
                task = q.task
                task.completed = True
                task.save()

        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'respondent/response.html', {'user': user, 'task': task, 'questions': questions})
