from respondent.models import GroupRespondent
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