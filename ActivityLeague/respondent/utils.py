from core.utils import get_responses
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
