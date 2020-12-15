from django.shortcuts import render, get_object_or_404
from .models import Interviewee

# Create your views here.
def dashboard(request, pk):
    user = get_object_or_404(Interviewee, pk=pk)
    return render(request, 'interviewee_dashboard.html', {'user' : user})

def leaderboard(request, pk):
    user = get_object_or_404(Interviewee, pk=pk)
    interviewees = Interviewee.objects.all()
    return render(request, 'interviewee_leaderboard.html', {'user' : user, 'interviewees' : interviewees})

def response(request, pk):
    user = get_object_or_404(Interviewee, pk=pk)
    return render(request, 'response.html', {'user' : user})

def login(request):
    return render(request, 'login.html')