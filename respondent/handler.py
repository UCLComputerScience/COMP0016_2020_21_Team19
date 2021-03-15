from django.utils import timezone

from core.utils import *
from core.models import Question
from .models import Response


"""
Contains functions designated to handle specific requests made to the views.
"""


def post_response(request, user):
    """
    Handles the POST request made by the ``Respondent`` by saving the ``Response``\s to the
    ``Task`` and marking the task as complete if they are the final ``Respondent``
    to complete the task.

    :param request: The POST Request made by the user when submitting responses to a task.
    :type request: django.http.HttpRequest
    """
    # get a list of Question IDs for which the user clicked the link
    links_clicked = [x for x in request.POST.get('clicked').split(',')]
    current_date_time = timezone.now()

    for question_id, data in request.POST.items():
        # don't need to process the csrf token or the array of clicked Question IDs
        if question_id == 'csrfmiddlewaretoken' or question_id == 'clicked':
            continue    
        
        question = Question.objects.get(id=question_id)
        _save_response(question, question_id, links_clicked, current_date_time, data, user)

        # mark completed if all respondents have completed the task
        questions = Question.objects.filter(task=question.task)
        num_responses = Response.objects.filter(question__in=questions).count()
        if num_responses == get_num_respondents_in_group(question.task.group) * questions.count():
            question.task.mark_as_complete()


def _save_response(question, question_id, links_clicked, current_date_time, data, user):
    """
    Saves a response by creating a ``Response`` object in the database.

    :param links_clicked: List of strings representing ``Question`` IDs that the user has
                            clicked the link of.
    :type links_clicked: List[str]
    :param current_date_time: The current date and time.
    :type current_date_time: ``datetime.datetime``
    :param data: The response to a specific question  (could be qualitative or quantitative).
    :type data: str
    :param question_id: The id of the ``Question`` to link the ``Response`` to.
    :type question_id: str
    """
    link_clicked = question_id in links_clicked
    
    # Ascending quantitative (higher is better)
    if question.is_ascending:
        Response.objects.create(question=question, respondent=user, value=float(data),
                                date_time=current_date_time, link_clicked=link_clicked)
    # Descending quantitative (lower is better)
    elif question.is_descending:
        Response.objects.create(question=question, respondent=user, value=6-float(data),
                                date_time=current_date_time, link_clicked=link_clicked)                          
    # Qualitative
    else:
        text_positive = None
        if not question.is_text_neutral:
            text_positive = question.is_text_positive
        Response.objects.create(question=question, respondent=user, text=data, date_time=current_date_time,
                                link_clicked=link_clicked, text_positive=text_positive)