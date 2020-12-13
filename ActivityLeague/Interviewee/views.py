from django.shortcuts import render
from .models import Interviewee

# Create your views here.
def dashboard(request, pk):
    user = Interviewee.objects.get(pk=pk)
    return render(request, 'interviewee_dashboard.html', {'user' : user})

def leaderboard(request, pk):
    user = Interviewee.objects.get(pk=pk)
    return render(request, 'interviewee_leaderboard.html', {'user' : user})

def response(request, pk):
    user = Interviewee.objects.get(pk=pk)
    return render(request, 'response.html', {'user' : user})

def login(request):
    return render(request, 'login.html')