import datetime
import operator

from respondent.models import Respondent, Response, GroupRespondent
from surveyor.models import Surveyor, GroupSurveyor, Group, Task, Question


def get_groups(user):
    """
    Returns the groups which the user is a member/manager of.

    Args:
        user (Surveyor/Respondent): Either a Surveyor or Respondent object
                                    representing the user currently logged in.

    Raises:
        ValueError: Raised if the user type specified is not recognised.

    Returns:
        list:Group : Groups managed by/participated in by the user.
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

    Args:
        user (Surveyor/Respondent): Logged in user.
        
    Kwargs:
        group (UUID): ID of the target group's leaderboard.

    Returns:
        list:dict : Sorted descending list containing the full names and scores of of the
                    members of the leaderboard.
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
    Retrieves labels for chart.js on respondent_progress_page.html based on
    the existing respondent's responses.
    
    Args:
        pk (int): Primary key of the respondent for which we are rendering a chart.

    Returns:
        list:str : Sorted list whose length is the smallest of the number of responses
               in a group or 10. Contains the string representations of the labels
               to be rendered on charts.
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


def get_graph_data(user, labels, **kwargs):
    """
    Retrieves the values to be plotted by Chart.js on respondent_progress_page.html.

    Args:
        pk (int): Primary key of the respondent whose progress we are to be
                  displaying.
        labels (list: string): List of string datetimes that are the labels
                               on the x-axis of the graph that to be displayed.
    
    Kwargs: 
        group (Group). If passed, this method shall return the progress
                       values for the labels for the group that is passed.
                       
    Returns:
        (list:num): List of values of length labels.length corresponding to the
                    values to be plotted.
    """
    responses = get_responses(user, **kwargs)

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
    return GroupRespondent.objects.filter(group=group).count()