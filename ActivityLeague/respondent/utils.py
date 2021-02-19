from core.utils import get_groups, get_graph_labels, get_graph_data, get_responses
import random

def random_hex_colour():
    random_n = random.randint(0, 16777215)
    hex_number = format(random_n, 'x')
    hex_number = '#' + hex_number
    return hex_number


def get_chartjs_dict(scores):
    return {'data': scores,
            'lineTension': 0,
            'backgroundColor': 'transparent',
            'borderColor': random_hex_colour(),
            'borderWidth': 4,
            'pointBackgroundColor': '#007bff'}


def get_progress_graphs(user):
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
