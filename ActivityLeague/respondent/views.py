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
    queryset = Response.objects.filter(pk=respondent)
    return queryset

def get_responses(pk):
    respondent = Respondent.objects.get(pk=pk)

    
@deprecation.deprecated("Deprecated for the purposes of testing whether all labels will load at once.")
def progress_labels(pk, num_intervals): # TODO: I am currently working here
    oldest_task_time = get_oldest_task(pk) # type datetime.date 
    newest_task_time = get_newest_task(pk)


def get_oldest_task(pk): # TODO: Handle case for empty queryset
    respondent = Respondent.objects.get(pk=pk)
    group_respondents = GroupRespondent.objects.get(respondent=respondent)
    group = Group.objects.get(pk=group_respondents.group_id)
    time = Task.objects.filter(group=group).order_by('due_date')[0]
    print(time.due_date)
    return time.due_date

def get_newest_task(pk): # TODO: Handle case for empty queryset
    respondent = Respondent.objects.get(pk=pk)
    group_respondents = GroupRespondent.objects.get(respondent=respondent)
    group = Group.objects.get(pk=group_respondents.group_id)
    time = Task.objects.filter(group=group).order_by('-due_date')[0]
    print(time.due_date)
    return time.due_date

def get_task_score(respondent, task): # TODO: Test this
    questions = Question.objects.filter(task=task)
    responses = Response.objects.filter(question=questions)
    print(responses)
    num_questions = 0
    for question in questions:
        num_questions += 1

def get_user_tasks(respondent):
    # TODO:
    pass