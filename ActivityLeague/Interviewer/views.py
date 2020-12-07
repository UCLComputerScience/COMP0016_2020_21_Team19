from django.shortcuts import render

def dashboard(request):
    return render(request, 'interviewer_dashboard.html')

def leaderboard(request):
    return render(request, 'interviewer_leaderboard.html')

def task_overview(request):
    return render(request, 'task_overview.html')

def new_task(request):
    return render(request, 'interviewer_new_task.html')