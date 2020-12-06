from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'interviewer_dashboard.html')

def leaderboard(request):
    return render(request, 'interviewer_leaderboard.html')

def task_overview(request):
    return render(request, 'task_overview.html')