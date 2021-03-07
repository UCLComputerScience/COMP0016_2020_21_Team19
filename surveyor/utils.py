import base64
import io
import urllib
from urllib.parse import urlparse

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from core.utils import *
from surveyor.models import Surveyor, QuestionTemplate, TaskTemplate


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
        labels = get_graph_labels(surveyor, group=group)
        scores = get_graph_data(surveyor, labels, group=group)
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


# TODO: Clean up
def get_questions(task_id):
    task = Task.objects.get(id=task_id)
    questions = Question.objects.filter(task=task)

    data = []
    for question in questions:
        responses = Response.objects.filter(question=question)
        pie_chart_labels = None
        pie_chart_data = None

        if question.response_type == 1:
            response_type = "likert"
            pie_chart_labels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]
        elif question.response_type == 2:
            response_type = "traffic"
            pie_chart_labels = ['Red', 'Yellow', 'Green']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 4)]
        elif question.response_type == 3:  # neutral text
            response_type = "text"
        elif question.response_type == 5:  # positive text
            response_type = "text"
        elif question.response_type == 6:  # negative text
            response_type = "text"
        elif question.response_type == 4:
            response_type = "numerical-radio"
            pie_chart_labels = ['1', '2', '3', '4', '5']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]

        word_cloud = None
        if response_type in ["text", "text-positive", "text-negative"]:
            word_cloud = create_word_cloud(responses)

        link_clicks = 0
        for response in responses:
            link_clicks += response.link_clicked

        data.append({
            'id': question.id,
            'link': question.link,
            'type': response_type,
            'description': question.description,
            'link_clicks': link_clicks,
            'pie_chart_labels': pie_chart_labels,
            'pie_chart_data': pie_chart_data,
            'word_cloud': word_cloud})

    return data


def get_overall_word_cloud(surveyor, respondent, text_positive=None):
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
    responses = responses.filter(text__isnull=False, text_positive=text_positive)  # get only text responses
    word_cloud = create_word_cloud(responses)
    return word_cloud

# def get_templates_and_questions(self, surveyor):
#     templates = TaskTemplate.objects.filter(surveyor=user)
#         questions = 
#         for template in templates:
#             questions = QuestionTemplate.objects.filter()
#     data = []
#     templates = TaskTemplate.objects.filter(surveyor=surveyor)
#     for template in templates:
#         entry = {QuestionTemplate.objects.filter}
    
#     return data