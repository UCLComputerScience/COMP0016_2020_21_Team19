import datetime
import enum

from django.shortcuts import get_object_or_404
from respondent.models import Respondent, Response, GroupRespondent
from surveyor.models import Surveyor, GroupSurveyor, Group


class UserType(enum.Enum):
    SURVEYOR = 1
    RESPONDENT = 2


def get_groups(user, user_type):
    """
    Returns the groups which the user is a member/manager of.

    Args:
        user (User): Django Auth User object associated with either a 
                     Surveyor or Respondent object.
        user_type (UserType): Instance of UserType used to determine
                              groups to be returned.

    Raises:
        ValueError: Raised if the user type specified is not recognised.

    Returns:
        list:Group : Groups managed by/participated in by the UserType.
    """
    if user_type == SURVEYOR:
        surveyor = Surveyor.objects.get(user=user)
        group_ids = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
    elif user_type == RESPONDENT:
        respondent = Respondent.objects.get(user=user)
        group_ids = GroupRespondent.objects.filter(respondent=respondent).values_list('group', flat=True)
    else:
        raise ValueError('UserType not recognised!')
    
    groups = Group.objects.filter(pk__in=group_ids)
    return groups

def get_leaderboard(user, user_type, **kwargs):
    """
    Retrieves a sorted list containing the names and scores of the members
    of the leaderboard.

    Args:
        user (User): Logged in user.
        user_type (UserType): Type of User associated with user: Surveyor or Respondent.
    
    Kwargs:
        group (UUID): ID of the target group's leaderboard.

    Returns:
        list:dict : Sorted descending list containing the full names and scores of of the
                members of the leaderboard.
    """
    
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        respondent_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    else:
        if user_type == SURVEYOR:
            groups = get_groups(user)
        elif user_type == RESPONDENT:
            respondent = Respondent.objects.get(user=user)
            groups = GroupRespondent.objects.filter(respondent=respondent).values_list('group', flat=True)
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
    
    if len(responses) == 0:
        return None
    
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
    
    assert(len(dates) == len(scores))
    return scores

# Surveyor
def get_responses(user, user_type, **kwargs):
    """
    Returns the responses associated with either a user, group, task or question.

    Args:
        user (User): Logged in user.
        user_type (UserType): Type of the user logged in.

    Returns:
        list:Response : Responses associated with a question, task, group or user. 
                        Ordered by the date and time that it is due.
    """
    surveyor = Surveyor.objects.get(user=user)
    if kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
    else:
        groups = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group',flat=True)
        tasks = Task.objects.filter(group__in=groups)
    questions = Question.objects.filter(task__in=tasks)
    return Response.objects.filter(question__in=questions).order_by('date_time')

# Respondent
def get_responses(user, **kwargs):
    respondent = Respondent.objects.get(user=user)
    if kwargs.get('task') is not None:
        task = kwargs.get('task')
        questions = Question.objects.filter(task=task)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date_time')
    elif kwargs.get('question') is not None:
        question = kwargs.get('question')
        return Response.objects.filter(respondent=respondent, question=question).order_by('date_time')
    elif kwargs.get('group') is not None:
        group = kwargs.get('group')
        tasks = Task.objects.filter(group=group)
        questions = Question.objects.filter(task__in=tasks)
        return Response.objects.filter(respondent=respondent, question__in=questions).order_by('date_time')
    else:
        return Response.objects.filter(respondent=respondent).order_by('date_time')