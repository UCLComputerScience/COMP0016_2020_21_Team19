from django.shortcuts import render
from .models import Interviewee

# Create your views here.
def dashboard(request):
    return render(request, 'interviewee_dashboard.html',)

def leaderboard(request):
    # jc = Interviewee.objects.create(firstname='Joseph', surname='Connor')
    # dm = Interviewee.objects.create(firstname='Dean', surname='Mohammedally')
    interviewees = Interviewee.objects.all()
    return render(request, 'interviewee_leaderboard.html', {'interviewees' : interviewees})

def response(request):
    return render(request, 'response.html')

def login(request):
    return render(request, 'login.html')
