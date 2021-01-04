from django.shortcuts import render, get_object_or_404
from .models import Respondent

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
    return render(request, 'respondent_progress_page.html', {'user' : user})

def response(request, pk):
    user = get_object_or_404(Respondent, pk=pk)
    return render(request, 'response.html', {'user' : user})
    # return render(request, 'response.html')

def login(request):
    return render(request, 'login.html')