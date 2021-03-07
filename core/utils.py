import datetime
import operator
import random

from respondent.models import Respondent, Response, GroupRespondent
from surveyor.models import Surveyor, GroupSurveyor, Group, Task, Question


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


def get_leaderboard(user, **kwargs):
    """
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

    if kwargs.get('group'):
        group = kwargs.get('group')
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        if isinstance(user, Surveyor):
            groups = get_groups(user)
        elif isinstance(user, Respondent):
            groups = GroupRespondent.objects.filter(respondent=user).values_list('group', flat=True)
        respondent_ids = GroupRespondent.objects.filter(group__in=groups).values_list('respondent', flat=True)

    respondents = Respondent.objects.filter(id__in=respondent_ids)

    rows = []
    for respondent in respondents:
        # Get their responses and calculate their score
        if isinstance(user, Surveyor):
            if  kwargs.get('group'):
                responses = get_responses(user, respondent=respondent, group=group).values_list('value', flat=True)
            else:
                responses = get_responses(user, respondent=respondent).values_list('value', flat=True)
        else:
            if kwargs.get('group'):
                responses = get_responses(respondent, group=group).values_list('value', flat=True)
            else:
                responses = get_responses(respondent).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': round(score, 2)}
        rows.append(entry)

    rows.sort(key=operator.itemgetter('score'), reverse=True)

    return rows


# Surveyor
def get_graph_labels(user, **kwargs):
    """
    Retrieves the x-axis labels (dates) used for progress graphs.

    :param user:  A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor or Respondent
    :return: A sorted list containing the dates to be used as x-axis labels.
    :rtype: List[str]
    """
    responses = get_responses(user, **kwargs)
    responses = responses.filter(value__isnull=False)

    if not responses:
        return []

    num_intervals = min(len(responses), 10)
    dates = list(responses.values_list('date_time', flat=True))
    dates = [date_time.date() for date_time in dates]

    latest = dates[-1]
    earliest = dates[0]
    time_range = latest - earliest

    interval = time_range / num_intervals

    labels = [str(earliest + (interval * i)) for i in range(num_intervals + 1)]

    return labels


def get_graph_data(user, labels, **kwargs):
    """
    Retrieves the data used for progress graphs on the dashboard and progress page.

    :param user: The ``Surveyor`` or ``Respondent`` whose progress is to be displayed.
    :type user: Surveyor or Respondent
    :param labels: List of string datetimes that are the labels on the 
                   x-axis of the graph that to be displayed.
    :Keyword Arguments:
        * *group* (``Group``) If passed, this method shall return the 
                              progress values for the labels for the 
                              group that is passed.
    :type labels: List[str]
    :return: List of values of length len(labels) corresponding to the
             values to be plotted.
    :rtype: List[float]
    """

    responses = get_responses(user, **kwargs)
    responses = responses.filter(value__isnull=False)

    if not responses:
        return []

    dates = [datetime.datetime.strptime(label, '%Y-%m-%d').date() for label in labels]

    if len(dates) == 0:
        return None

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

    assert (len(dates) == len(scores))
    return scores


# Surveyor
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

    if isinstance(user, Surveyor):
        responses = Response.objects.all()
    else:
        responses = Response.objects.filter(respondent=user)

    if kwargs.get('group'):
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
        questions = Question.objects.filter(task__in=tasks)
        responses = responses.filter(question__in=questions)
    elif kwargs.get('task'):
        task = kwargs.get('task')
        questions = Question.objects.filter(task=task)
        responses = responses.filter(question__in=questions)
    elif kwargs.get('question'):
        question = kwargs.get('question')
        questions = Question.objects.filter(id=question.id)  # wrap object in queryset
        responses = responses.filter(question__in=questions)

    if kwargs.get('respondent'):
        respondent = kwargs.get('respondent')
        groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
        tasks = Task.objects.filter(group__in=groups)
        questions = Question.objects.filter(task__in=tasks)
        return responses.filter(respondent=respondent, question__in=questions).order_by('date_time')
        
    if not kwargs:
        if isinstance(user, Respondent):
            return responses.order_by('date_time')
        else:
            groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
            tasks = Task.objects.filter(group__in=groups)
            questions = Question.objects.filter(task__in=tasks)
            responses = responses.filter(question__in=questions)

    return responses.order_by('date_time')


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
    elif isinstance(user, Respondent):
        groups = GroupRespondent.objects.filter(respondent=user).values_list('group', flat=True)
    tasks = Task.objects.filter(group__in=groups).order_by('due_date', 'due_time')
    if isinstance(user, Respondent):
        tasks = list(filter(lambda task: not get_responses(user, task=task), tasks))
    now = datetime.datetime.now()
    for task in tasks:
        if isinstance(user, Surveyor):
            questions = Question.objects.filter(task=task)
            responses = Response.objects.filter(question__in=questions)
            task.num_group_respondents = get_num_respondents_in_group(task.group)
            task.num_responses = responses.count() // questions.count()
        task.due_dt = datetime.datetime.combine(task.due_date, task.due_time)
        until = task.due_dt - now
        task.color = "red" if until < datetime.timedelta(days=1) else "orange" if until < datetime.timedelta(
            days=2) else "darkgreen"
    return tasks, now


def get_num_respondents_in_group(group):
    """
    Gets the number of ``Respondent``\s in a given ``Group``.

    :param group: The group from which to count the number of ``Respondent``\s.
    :type group: Group
    :return: The number of ``Respondent``\s in the ``Group``.
    :rtype: int
    """
    return GroupRespondent.objects.filter(group=group).count()


def random_hex_colour():
    """
    Generates a random hex colour code between 0x000000 and 0xFFFFFF.

    :return: 6-digit hexadecimal code.
    :rtype: str
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def get_chartjs_dict(values):
    """
    Wraps a list of values in a dictionary in the correct format for a Chart.js line chart.

    :param values: A list of values to use as a dataset for the line chart.
    :type values: List[float]
    :return: A dictionary representing a dataset for a Chart.js line chart.
    :rtype: dict
    """
    colour = random_hex_colour()
    return {'data': values,
            'lineTension': 0,
            'backgroundColor': 'transparent',
            'borderColor': colour,
            'borderWidth': 4,
            'pointBackgroundColor': colour}


def get_progress_graphs(respondent):
    """
    Gets the graph data for all of the ``Group``\s the ``Respondent`` is in.

    :param respondent: The ``Respondent`` to get graph data for.
    :type respondent: Respondent
    :return: A list of dictionaries, where each dictionary contains data for the progress graph for an individual group.
    :rtype: List[dict]
    """
    groups = get_groups(respondent)
    overall_labels = get_graph_labels(respondent)

    group_graphs = []
    overall_data = []
    for group in groups:
        group_labels = get_graph_labels(respondent, group=group)
        group_scores = get_graph_data(respondent, group_labels, group=group)
        group_title = group.name
        group_graphs.append(
            {'id': group.id, 'title': group_title, 'labels': group_labels, 'scores': [get_chartjs_dict(group_scores)]})
        overall_data.append(get_chartjs_dict(group_scores))

    overall = {'id': 'overall', 'title': 'Overall', 'labels': overall_labels, 'scores': overall_data}
    group_graphs.insert(0, overall)

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
