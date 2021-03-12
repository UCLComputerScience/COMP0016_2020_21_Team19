import datetime
import operator

from django.db.models import Avg
from django.utils import timezone

from respondent.models import Respondent, Response, GroupRespondent
from surveyor.models import Surveyor, GroupSurveyor
from .models import Group, Task, Question


def get_groups(user):
    """
    Retrieves the ``Group``\s which the user is a manager/member of.
    
    :param user: A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor or Respondent
    :raises ValueError: Raised if the user type specified is not recognised.
    :return: A ``QuerySet`` of the ``Group``\s which `user` manages or is a member of.
    :rtype: django.db.models.QuerySet
    """
    if isinstance(user, Surveyor):
        group_ids = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
    elif isinstance(user, Respondent):
        group_ids = GroupRespondent.objects.filter(respondent=user).values_list('group', flat=True)
    else:
        raise ValueError('User type not recognised!')

    groups = Group.objects.filter(id__in=group_ids)
    return groups


def get_leaderboard(user, group=None):
    """group"
    Retrieves a sorted list containing the names and scores of the members
    of the leaderboard.

    :param user:  A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor or Respondent
    :Keyword Arguments:
        * *group* (``uuid.UUID``) The ``UUID`` of the ``Group`` for which `user` is accessing the leaderboard.
    :return: Sorted descending list containing the full names and scores of of the members 
             of the leaderboard.
    :rtype: List[dict]
    """

    if group:
        group = group
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        groups = get_groups(user)
        respondent_ids = GroupRespondent.objects.filter(group__in=groups).values_list('respondent', flat=True)

    # Get the respondents in the group(s) we want to show the leaderboard for
    respondents = Respondent.objects.filter(id__in=respondent_ids)

    rows = []
    for respondent in respondents:
        # Get their responses and calculate their score
        if isinstance(user, Surveyor):
            responses = get_responses(user, group=group, respondent=respondent).values_list('value', flat=True)
        else:
            responses = get_responses(respondent, group=group).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': round(score, 2)}
        rows.append(entry)
    rows.sort(key=operator.itemgetter('score'), reverse=True)
    return rows


def get_chart_data(user, **kwargs):
    """
    Returns the scores and labels to be displayed any time a graph is being displayed using Chart.js.

    :param user: A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :Keyword Arguments:
        * *group* (``Group``) If passed, this method shall return the scores and labels for an entire group.
    :return: A tuple containing a list of labels (represented as epoch time), whereby a single label
             represents a single day, and a list of scores (represented as floats) whereby a single score
             represents the rolling average of the user until that day.
    :rtype: tuple(List, List)
    """
    responses = get_responses(user, **kwargs)
    responses = responses.filter(value__isnull=False)  # Filter out text responses

    if not responses:
        return [], []

    x_date, y_score = [], []

    date = responses.first().date_time
    end = timezone.now()

    while date <= end:
        rolling_avg = responses.filter(date_time__lte=date + datetime.timedelta(days=1)).aggregate(Avg('value'))[
            'value__avg']
        date_to_datetime = datetime.datetime.combine(date.date(), datetime.time())
        milliseconds = date_to_datetime.timestamp() * 1000
        x_date.append(milliseconds)
        y_score.append(rolling_avg)
        date += datetime.timedelta(days=1)

    return x_date, y_score


def get_responses(user, **kwargs):
    """
    Retrieves the responses for a user, in accordance with the specified keyword arguments.
    For example, if ``user`` is of type ``Respondent`` and ``group`` is a keyword argument which specifies a ``Group``,
    this method returns a ``QuerySet`` of ``Group``\s which the ``Respondent`` is a member of.

    :param user: A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor or Respondent
    :Keyword Arguments:
        * *group* (``Group``) If passed, this method shall return the 
                              ``Response``\s associated with the given ``Group``
        * *task* (``Task``) If passed, this method shall return the 
                            ``Response``\s associated with the given ``Task``
        * *question* (``Question``) If passed, this method shall return the 
                                    ``Response``\s associated with the given ``Question``
        * *respondent* (``Respondent``) If passed, this method shall return the 
                                        ``Response``\s associated with the given ``Respondent``
    :return: A ``QuerySet`` of ``Group``\s as determined by the user type and in accordance with the specified keyword arguments.
    :rtype: django.db.models.QuerySet
    """

    if kwargs.get('group'):
        responses = _get_responses_by_group(kwargs.get('group'))
    elif kwargs.get('task'):
        responses = _get_responses_by_task(kwargs.get('task'))
    elif kwargs.get('question'):
        responses = _get_responses_by_question(kwargs.get('question'))
    else:
        responses = Response.objects.all()

    if isinstance(user, Surveyor):
        responses = _filter_responses_by_surveyor(responses, user)
        if kwargs.get('respondent'):
            respondent = kwargs.get('respondent')
            responses = responses.filter(respondent=respondent)
    else:
        responses = responses.filter(respondent=user)

    return responses.order_by('date_time')


def _filter_responses_by_surveyor(responses, surveyor):
    """
    Filters a ``QuerySet`` of ``Response``\s to contain only ``Response``\s submitted to
    ``Task``s created by the given `surveyor`.

    :param responses: The ``QuerySet`` of ``Response``\s to filter.
    :type responses: django.db.models.QuerySet
    :param surveyor: The ``Surveyor`` to filter the ``Response``\s by.
    :type surveyor: ``Surveyor``
    :return: A ``QuerySet`` containing all of the ``Response``\s to all of the ``Questions`` in all of the
            ``Task``\s in all of the ``Group``\s that are managed by `surveyor`.
    :rtype: django.db.models.QuerySet
    """
    questions = _get_questions_by_surveyor(surveyor)
    return responses.filter(question__in=questions)


def _get_questions_by_surveyor(surveyor):
    """
    Returns a ``QuerySet`` of ``Questions``\s created by the given `surveyor`.

    :param surveyor: The ``Surveyor`` of whom to create the ``Task``s of.
    :type surveyor: ``Surveyor``
    :return: A ``QuerySet`` containing all of the ``Questions``\s created by the given `surevyor`.
    :rtype: django.db.models.QuerySet
    """
    groups = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    tasks = Task.objects.filter(group__in=groups)
    questions = Question.objects.filter(task__in=tasks)
    return questions


def _get_responses_by_respondent(respondent, surveyor):
    """
    Returns a ``QuerySet`` of ``Response``\s containing only ``Response``\s submitted by the given `respondent`,
    and submitted to a ``Task`` set by the given `surveyor`.

    :param respondent: The ``Respondent`` to get the ``Response``\s of.
    :type respondent: ``Respondent``
    :param surveyor: The ``Surveyor`` which set the tasks to the respondent.
    :type surveyor: ``Surveyor``
    :return: A ``QuerySet`` containing all of the ``Response``\s made by the given `respondent` to all of the ``Questions`` in all of the
            ``Task``\s in all of the ``Group``\s that are managed by `surveyor`.
    :rtype: django.db.models.QuerySet
    """
    questions = _get_questions_by_surveyor(surveyor)
    return Response.objects.filter(respondent=respondent, question__in=questions)


def _get_responses_by_question(question):
    """
    Returns a ``QuerySet`` of ``Response``\s containing only ``Response``\s submitted to the given `question`.

    :param question: The ``Question`` to get the responses to.
    :type question: ``Question``
    :return: A ``QuerySet`` containing all of the ``Response``\s to `question`.
    :rtype: django.db.models.QuerySet
    """
    questions = Question.objects.filter(id=question.id)  # wrap object in queryset
    return Response.objects.filter(question__in=questions)


def _get_responses_by_task(task):
    """
    Returns a ``QuerySet`` of ``Response``\s containing only ``Response``\s submitted to the given `task`.

    :param question: The ``Question`` with which to filter responses
    :type task: ``Task``
    :return: A ``QuerySet`` containing all of the ``Response``\s to all of the ``Question``\s in `task`.
    :rtype: django.db.models.QuerySet
    """
    questions = Question.objects.filter(task=task)
    return Response.objects.filter(question__in=questions)


def _get_responses_by_group(group):
    """
    Returns a ``QuerySet`` of ``Response``\s containing only ``Response``\s submitted by members of the given `group`.

    :param group:
    :type group: ``Group``
    :return: A ``QuerySet`` of all ``Response``\s submitted by members of the given `group`.
    :rtype: django.db.models.QuerySet
    """
    tasks = Task.objects.filter(group=group)
    questions = Question.objects.filter(task__in=tasks)
    return Response.objects.filter(question__in=questions)


def calculate_score(values):
    """
    Calculates the average (mean) of a set of values.

    :param values: The values from which to determine an average from.
    :type values: List[int]
    :return: The average (mean) of the values.
    :rtype: float
    """
    values = list(filter(lambda value: value, values))
    return 0 if not len(values) else sum(values) / len(values)


def get_tasks(user):
    """
    Retrieves the tasks for a user, and a ``datetime`` instance representing the current date and time.
    If ``user`` is of type ``Surveyor``, this method returns the tasks that they created.
    If ``user`` is of type ``Respondent``, this method returns the tasks that they have been assigned.

    :param user: A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor or Respondent
    :return: A ``QuerySet`` of the tasks and the ``datetime`` instance representing the current date and time.
    :rtype: (django.db.models.QuerySet, datetime.datetime)
    """
    if isinstance(user, Surveyor):
        groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
    else:
        groups = GroupRespondent.objects.filter(respondent=user).values_list('group', flat=True)
    tasks = Task.objects.filter(group__in=groups).order_by('due_date', 'due_time')

    if isinstance(user, Respondent):
        tasks = list(filter(lambda task: not get_responses(user, task=task), tasks))
    now = datetime.datetime.now()
    for task in tasks:
        if isinstance(user, Surveyor):
            task = _set_task_attrs(task, now)
        task.due_dt = datetime.datetime.combine(task.due_date, task.due_time)
        until = task.due_dt - now
        task.color = "red" if until < datetime.timedelta(days=1) else "orange" if until < datetime.timedelta(days=2) \
            else "darkgreen"
    return tasks, now


def _set_task_attrs(task, now):
    """
    Returns `task` with additional attributes to be displayed about the task in the rendered template,
    including: the number of responses to the task, the due date of the task and the colour to display
    the due date of the task in.

    :param task: The ``Task`` to set the display attributes of.
    :type task: ``Task``
    :param now: The ``datetime.datetime`` object representing the current date and time.
    :type now: ``datetime.datetime``
    :return: The ``Task`` with attributes which are used in the template.
    :rtype: ``Task``
    """

    questions = Question.objects.filter(task=task)
    responses = Response.objects.filter(question__in=questions)
    task.num_group_respondents = get_num_respondents_in_group(task.group)
    task.num_responses = responses.count() // questions.count()
    return task


def get_num_respondents_in_group(group):
    """
    Gets the number of ``Respondent``\s in a given ``Group``.

    :param group: The group from which to count the number of ``Respondent``\s.
    :type group: Group
    :return: The number of ``Respondent``\s in the ``Group``.
    :rtype: int
    """
    return GroupRespondent.objects.filter(group=group).count()


def get_progress_graphs(respondent):
    """
    Gets the graph data for all of the ``Group``\s the ``Respondent`` is in.

    :param respondent: The ``Respondent`` to get graph data for.
    :type respondent: Respondent
    :return: A list of dictionaries, where each dictionary contains data for the progress graph for an individual group.
    :rtype: List[dict]
    """
    groups = get_groups(respondent)

    group_graphs = []
    for group in groups:
        group_labels, group_scores = get_chart_data(respondent, group=group)
        group_graphs.append(
            {'id': group.id, 'title': group.name, 'labels': group_labels, 'scores': group_scores})

    return group_graphs


def has_responded_to_task(respondent, task):
    """
    Returns a boolean value representing if a certain ``Respondent`` has responded
    to a given ``Task``.

    :param respondent: The ``Respondent`` for which to check ``Response``\s from.
    :type respondent: Respondent
    :param task: The ``Task`` for which to check ``Response``\s to.
    :type task: Task
    :return: Returns ``True`` if the number of ``Response``\s to the given ``Task`` is equal to the number of ``Question``\s, ``False`` otherwise
    :rtype: bool
    """
    questions = Question.objects.filter(task=task)
    responses = Response.objects.filter(respondent=respondent, question__in=questions)
    return len(responses) == len(questions)
