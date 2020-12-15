from django.shortcuts import render, get_object_or_404
from .forms import TaskForm, QuestionFormset
from .models import *


def dashboard(request, pk):
    user = get_object_or_404(Interviewer, pk=pk)
    return render(request, 'interviewer_dashboard.html', {'user' : user})

def leaderboard(request, pk):
    user = get_object_or_404(Interviewer, pk=pk)
    return render(request, 'interviewer_leaderboard.html', {'user' : user})

def task_overview(request, pk):
    user = get_object_or_404(Interviewer, pk=pk)
    return render(request, 'task_overview.html', {'user' : user})

def new_task(request, pk):
    # Create new task with questions
    user = get_object_or_404(Interviewer, pk=pk)
    group_interviewers = GroupInterviewer.objects.filter(interviewer_id=pk)
    groups = []
    for gr in group_interviewers:
        groups.append(Group.objects.get(pk=gr.id))

    if request.method == 'GET':
        form = TaskForm(request.GET or None)
        formset = QuestionFormset(queryset=Question.objects.none())
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        formset = QuestionFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)

            for question_form in formset:
                question = question_form.save(commit=False)
                question.task_id = task
                question.save()

            task.title = form.cleaned_data['title']
            task.due_date = form.cleaned_data['date']
            task.group_id = Groups.objects.get(name=form.cleaned_data['group'])
            task.save()
            # task = Task.objects.create(
            #     title=form.cleaned_data.get('message'),
            #     topic=topic,
            #     created_by=user
            # )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTaskForm()

    return render(request, 'interviewer_new_task.html', {'user' : user, 'groups' : groups, 'taskform': form, 'formset': formset})