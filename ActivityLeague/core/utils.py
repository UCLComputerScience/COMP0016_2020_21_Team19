import datetime
import operator
import pytz
import random

from respondent.models import Respondent, Response, GroupRespondent
from surveyor.models import Surveyor, GroupSurveyor, Group, Task, Question


def get_groups(user):
    """
    Retrieves the ``Group``\s which the user is a manager/member of.
    
    :param user: A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor / Respondent
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

    groups = Group.objects.filter(pk__in=group_ids)
    return groups


def get_leaderboard(user, **kwargs):
    """
    Retrieves a sorted list containing the names and scores of the members
    of the leaderboard.

    :param user:  A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor / Respondent
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

    respondents = Respondent.objects.filter(pk__in=respondent_ids)

    rows = []
    for respondent in respondents:
        # Get their responses and calculate their score
        responses = Response.objects.filter(respondent=respondent).values_list('value', flat=True)
        score = calculate_score(responses)
        entry = {'name': respondent.firstname + " " + respondent.surname, 'score': score}
        rows.append(entry)

    rows.sort(key=operator.itemgetter('score'), reverse=True)

    return rows


# Surveyor
def get_graph_labels(user, **kwargs):
    """
    Retrieves the x-axis labels (dates) used for progress graphs.

    :param user:  A ``Surveyor``/``Respondent`` representing the user currently logged in.
    :type user: Surveyor / Respondent
    :return: A sorted list containing the dates to be used as x-axis labels.
    :rtype: List[str]
    """    
    responses = get_responses(user, **kwargs)

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


def get_graph_data(respondent, labels, **kwargs):
    """
    Retrieves the data used for progress graphs.

    :param respondent: The ``Respondent`` whose progress is to be displayed.
    :type respondent: ``Respondent``
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
    responses = get_responses(respondent, **kwargs)

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

    :param user: [description]
    :type user: [type]
    :return: [description]
    :rtype: [type]
    """    
    """
    Returns the responses associated with either a user, group, task or question.
    Args:
        user (Surveyor/Respondent): Logged in user.
    Returns:
        list:Response : Responses associated with a question, task, group or user.
                        Ordered by the date and time that it is due.
    """

    if isinstance(user, Surveyor):
        responses = Response.objects.all()
    else:
        responses = Response.objects.filter(respondent=user)

    if kwargs.get('group'):
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
        questions = Question.objects.filter(task__in=tasks)
    elif kwargs.get('task'):
        task = kwargs.get('task')
        questions = Question.objects.filter(task=task)
    elif kwargs.get('question'):
        question = kwargs.get('question')
        questions = Question.objects.filter(id=question.id)  # wrap object in queryset
    elif kwargs.get('respondent'):
        respondent = kwargs.get('respondent')
        groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
        tasks = Task.objects.filter(group__in=groups)
        questions = Question.objects.filter(task__in=tasks)
    else:
        if isinstance(user, Respondent):
            return responses.order_by('date_time')
        else:
            groups = GroupSurveyor.objects.filter(surveyor=user).values_list('group', flat=True)
            tasks = Task.objects.filter(group__in=groups)
            questions = Question.objects.filter(task__in=tasks)

    return responses.filter(question__in=questions).order_by('date_time')


def calculate_score(values):
    """
    The function calculating the scores of numerical/quantifiable responses
    for every ``Respondent``.

    :param values: [description]
    :type values: [type]
    :return: [description]
    :rtype: [type]
    """    
    """
    Args:
        values: List of numbers from which you want to calculate a score.

    Returns:
        int : The average score.
    """
    values = list(filter(lambda value: value, values))
    return 0 if not len(values) else sum(values) / len(values)


def get_tasks(user):
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
        task.color = "red" if until < datetime.timedelta(days=1) else "orange" if until < datetime.timedelta(days=2) else "darkgreen"
    return tasks, now


def get_num_respondents_in_group(group):
    """[summary]

    :param group: [description]
    :type group: [type]
    :return: [description]
    :rtype: [type]
    """    
    return GroupRespondent.objects.filter(group=group).count()


def random_hex_colour():
    """[summary]

    :return: [description]
    :rtype: [type]
    """    
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def get_chartjs_dict(scores):
    """[summary]

    :param scores: [description]
    :type scores: [type]
    :return: [description]
    :rtype: [type]
    """    
    return {'data': scores,
            'lineTension': 0,
            'backgroundColor': 'transparent',
            'borderColor': random_hex_colour(),
            'borderWidth': 4,
            'pointBackgroundColor': '#007bff'}


def get_progress_graphs(user):
    """
    When user is a ``Surveyor``, get graph data for all of the ``Group``\s managed by the ``Surveyor``.
    When user is a ``Respondent``, get graph data for all of the ``Group``\s the ``Respondent`` is in.

    :param user: The ``Surveyor`` or ``Respondent`` to get graph data for.
    :type user: Surveyor / Respondent
    :return: [description]
    :rtype: List[dict]
    """    
    groups = get_groups(user)
    overall_labels = get_graph_labels(user)

    group_graphs = []
    overall_data = []
    for group in groups:
        group_labels = get_graph_labels(user, group=group)
        group_scores = get_graph_data(user, group_labels, group=group)
        group_title = group.name
        group_graphs.append({'id' : group.id, 'title': group_title, 'labels': group_labels, 'scores': [get_chartjs_dict(group_scores)]})

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
    :return: Returns ``True` if the number of ``Response``\s to the given ``Task`` is equal to the number of ``Question``\s, ``False`` otherwise
    :rtype: bool
    """    
    questions = Question.objects.filter(task=task)
    responses = Response.objects.filter(respondent=respondent, question__in=questions)
    return len(responses) == len(questions)