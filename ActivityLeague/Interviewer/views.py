from django.shortcuts import render, get_object_or_404
from .models import Interviewer


def dashboard(request, pk):
    user = Interviewer.objects.get(pk=pk)
    return render(request, 'interviewer_dashboard.html', {'user' : user})

def leaderboard(request, pk):
    user = Interviewer.objects.get(pk=pk)
    return render(request, 'interviewer_leaderboard.html', {'user' : user})

def task_overview(request):
    return render(request, 'task_overview.html')

def new_task(request):
    return render(request, 'interviewer_new_task.html')