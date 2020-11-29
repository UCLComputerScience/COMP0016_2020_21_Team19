from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html',)

def leaderboard(request):
    return render(request, 'leaderboard.html')

def response(request):
    return render(request, 'response.html')

def login(request):
    return render(request, 'login.html')
