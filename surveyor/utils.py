import base64
import io
import urllib
from urllib.parse import urlparse

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from core.models import Question
from core.utils import *
from surveyor.models import Surveyor


def get_graphs_and_leaderboards(surveyor):
    """
    Retrieves a list of dictionaries containing the `labels`, `scores`, `leaderboards` and 
    `groups` required to render the graphs and leaderboards for every group the `surveyor`
    manages.

    :param surveyor: The ``Surveyor`` object representing the user that is currently logged in.
    :type surveyor: Surveyor
    :return: A list of dictionaries containing the `id`, `title`, `labels`, `scores` and `leaderboard`
             of every group managed by the currently logged in user.
    :rtype: List[dict]
    """
    groups = get_groups(surveyor).order_by('name')
    group_data = []
    for group in groups:
        labels, scores = get_chart_data(surveyor, group=group)
        group_data.append({'id': group.id, 'title': group.name, 'labels': labels, 'scores': scores,
                           'leaderboard': get_leaderboard(surveyor, group=group)})

    return group_data


def sanitize_link(url):
    """
    Removes the protocol from the given URL.

    :param url: The URL to be sanitized
    :type url: str
    :return: The sanitized URL.
    :rtype: str
    """
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


def create_word_cloud(responses):
    """
    Creates a word cloud from an iterable set of ``Response``\s.
    ``Response.text`` is not null for each ``Response``.

    :param responses: The ``Responses`` from which to create the word cloud.
    :type responses: iterable[Response]
    :return: A string representing the path of the bytestream of the word cloud image.
    :rtype: str
    """
    word_cloud_dict = {}
    for response in responses:
        word = response.text
        word_cloud_dict[word] = word_cloud_dict.get(word, 0) + 1

    if not word_cloud_dict:
        return None

    word_cloud = WordCloud(background_color=None, mode="RGBA").generate_from_frequencies(word_cloud_dict)
    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    buf.close()
    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64


def get_group_participants(group):
    """
    Returns a ``django.db.models.QuerySet`` of the ``Respondent`` objects which represent the participants of `group`.

    :param group: The ``Group`` representing the group whose participants the method shall be querying.
    :type group: Group
    :return: A ``QuerySet`` of the ``Respondent`` objects who are part of `group`.
    :rtype: django.db.models.QuerySet
    """
    group_respondents = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    return Respondent.objects.filter(id__in=group_respondents)


def get_task_summary(task_id):
    """
    Returns a summary of the responses to, and statistics about the ``Task`` with the given `task_id`.

    :param task_id: String representation of the UUID of the ``Task`` in question.
    :type task_id: str
    :return: A list of dictionaries containing, for each ``Question`` in the ``Task``, the
             question itself, the number of link clicks for each question, the labels and
             data for the chart for each question (if applicable) and the word cloud (if 
             applicable).
    :rtype: List[dict]
    """
    task = Task.objects.get(id=task_id)
    questions = Question.objects.filter(task=task)

    data = []
    for i, question in enumerate(questions):
        responses = Response.objects.filter(question=question)
        data.append({
            'question': question,
            'link_clicks': _get_question_link_clicks(responses),
            'chart_labels': question.get_labels(),
            'chart_data': _get_question_summary(question, responses)})

    return data


def get_word_cloud(surveyor, respondent, text_positive=None):
    """
    Gets the combined word cloud for the all of the text responses given by a certain ``Respondent`` to tasks
    set by a given ``Surveyor``.

    :param surveyor: The ``Surveyor`` for which to get responses for.
    :type surveyor: Surveyor
    :param respondent: The ``Respondent`` for which to get responses from.
    :type respondent: Respondent
    :param text_positive: Set to True if you want to collect strictly positive responses. Set to False
                          if you want strictly negative reponses and set to None (or leave blank) if you
                          want to collect responses which are neutral. 
    :type respondent: bool
    :return: A string representing the path of the bytestream of the word cloud image.
    :rtype: str
    """
    groups = get_groups(surveyor)
    responses = get_responses(surveyor, respondent=respondent)
    # get only text responses
    responses = responses.filter(text__isnull=False, text_positive=text_positive)
    word_cloud = create_word_cloud(responses)
    return word_cloud


def _get_question_summary(question, responses):
    """
    Returns a summary of the responses to `question`, including the number of responses,
    word cloud (if applicable). Textual/qualitative responses include word clouds, 
    quantitative responses include chart labels and response distributions.

    :param question: The ``Question`` to retrieve the summary for.
    :type question: ``Question``
    :param responses: The ``Response``\s to the given `question`.
    :type responses: django.db.models.QuerySet
    :return: For a quantitative response, this returns a list of values corresponding to
             the response  distribution to `question`. For qualitative responses, this
             returns the link to a word cloud.
    :rtype: List[int] or str
    """
    chart_data = None

    if question.is_ascending:
        chart_data = [responses.filter(value=i).count() for i in question.get_values_list()]
    elif question.is_descending:
        chart_data = [responses.filter(value=6-i).count() for i in question.get_values_list()]
    elif question.is_text:
        chart_data = create_word_cloud(responses)
    return chart_data


def _get_question_link_clicks(responses):
    """
    Returns the number of times the provided link for a ``Question`` was clicked
    by all the ``Respondent``\s who answered that ``Question``. The method calculates this
    from the ``QuerySet`` of all the ``Response``\s to a ``Question``.
    
    :param responses: The set of responses to a question from which to calculate the
                      number of link clicks.
    :type responses: django.db.models.QuerySet
    :return: The number of times the link was clicked.
    :rtype: int
    """
    return sum(response.link_clicked for response in responses)
