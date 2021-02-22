from respondent.models import GroupRespondent, Respondent, Response
from surveyor.models import Task, Question, Surveyor
from core.utils import get_groups, get_graph_labels, get_graph_data, get_leaderboard

from urllib.parse import urlparse
from wordcloud import WordCloud
from PIL import Image
import io
import base64
import urllib
import matplotlib.pyplot as plt

def get_graphs_and_leaderboards(user):
    groups = get_groups(user).order_by('name')
    group_data = []
    for group in groups:
        labels = get_graph_labels(user, group=group)
        scores = get_graph_data(user, labels, group=group)
        group_data.append({'id': group.id,'title': group.name, 'labels': labels, 'scores': scores, 'leaderboard': get_leaderboard(user, group=group)})
    
    return group_data

def sanitize_link(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)

def create_word_cloud(word_cloud_dict):
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
    group_respondents = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
    return Respondent.objects.filter(pk__in=group_respondents)

def get_questions(pk_task):
    task = Task.objects.get(pk=pk_task)
    questions = Question.objects.filter(task=task)
    
    data = []
    for question in questions:
        link_clicks = 0
        responses = Response.objects.filter(question=question)
        pie_chart_labels = None
        pie_chart_data = None
        word_cloud = None

        if question.response_type == 1:
            response_type = "likert"
            pie_chart_labels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]
        elif question.response_type == 2:
            response_type = "traffic"
            pie_chart_labels = ['Red', 'Yellow', 'Green']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 4)]
        elif question.response_type == 3:
            response_type = "text"
        elif question.response_type == 4:
            response_type = "numerical-radio"
            pie_chart_labels = ['1', '2', '3', '4', '5']
            pie_chart_data = [responses.filter(value=i).count() for i in range(1, 6)]
        else:
            response_type = None
        
        if response_type == "text":
            word_cloud_dict = {}
            for response in responses:
                link_clicks += response.link_clicked
                word = response.text
                word_cloud_dict[word] = word_cloud_dict.get(word, 0) + 1
            if word_cloud_dict:
                word_cloud = create_word_cloud(word_cloud_dict)
        else:
            for response in responses:
                link_clicks += response.link_clicked
        
        data.append({
            'id' : question.id,
            'link': question.link,
            'type': response_type,
            'description': question.description,
            'link_clicks': link_clicks,
            'pie_chart_labels': pie_chart_labels,
            'pie_chart_data': pie_chart_data,
            'word_cloud': word_cloud})

    return data