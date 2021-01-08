from django.shortcuts import render, get_object_or_404
from .models import *
from surveyor.models import *

# Create your views here.
def dashboard(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    return render(request, 'respondent_dashboard.html', {'user' : user})
    # return render(request, 'respondent_dashboard.html')

def leaderboard(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    respondents = Respondent.objects.all()
    return render(request, 'respondent_leaderboard.html', {'user' : user, 'respondents' : respondents})
    # return render(request, 'respondent_leaderboard.html')

def progress(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    progress_labels(pk, 5)
    return render(request, 'respondent_progress_page.html', {'user' : user})

def response(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    return render(request, 'response.html', {'user' : user})
    # return render(request, 'response.html')

def login(request):
    return render(request, 'login.html')

def get_progress_labels(pk, **kwargs):
    respondent = Respondent.objects.get(pk=pk)
    queryset = Response.objects.get(respondent=respondent)
    return queryset

def get_responses(pk, **kwargs):
    respondent = Respondent.objects.get(pk=pk)
    if kwargs.get('task') is not None: # TODO
        task = kwargs.get('task')
        # return Response.objects.select_related()
        pass

    elif kwargs.get('question') is not None: # TODO
        question = kwargs.get('question')
        pass
    else:
        return Response.objects.filter(respondent=respondent)

def get_tasks(pk):
    respondent = Respondent.objects.get(pk=pk)
    group_respondent = GroupRespondent.objects.get(respondent=respondent)
    return Task.objects.filter(group=group_respondent.group)

def get_response_values(pk):
    """
    :param pk: Primary key of the Respondent object for which you want to obtain
               the quantitative response values.
    """
    responses = get_responses(pk)
    dates = []
    scores = []
    for response in responses:
        pass


def calculate_score(responses):
    """
    :param responses: QuerySet of Repsonse objects of which you want to calculate
                      a score from. Only contains responses from fields that are
                      quantitative (e.g. likert responses), NOT qualitative (eg.
                      text responses).
    """
    score = 0
    n_questions = 0
    for response in responses:
        score += response.value
        n_questions += 1
    return score / n_questions