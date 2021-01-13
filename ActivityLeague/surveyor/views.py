from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import GroupForm, TaskForm, QuestionFormset
from .models import *


def dashboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_dashboard.html', {'user' : user})
    # return render(request, 'surveyor_dashboard.html')

def leaderboard(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'surveyor_leaderboard.html', {'user' : user})
    # return render(request, 'surveyor_leaderboard.html')

def task_overview(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    return render(request, 'task_overview.html', {'user' : user})
    # return render(request, 'task_overview.html')

def new_task(request, pk):
    user = get_object_or_404(Surveyor, pk=pk)
    group_surveyors = GroupSurveyor.objects.filter(surveyor_id=pk)
    groups = []

    for gr in group_surveyors:
        groups.append(Group.objects.get(pk=gr.id))

    if request.method == 'GET':
        form = TaskForm(request.GET or None)
        formset = QuestionFormset(queryset=Question.objects.none())
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        formset = QuestionFormset(request.POST)
        # if form.is_valid() and formset.is_valid():
        print("Valid form" if form.is_valid() else "Invalid form")
        print(form.errors)
        if True:
            task = form.save(commit=False)
            task.save()

            for question_form in formset:
                question = question_form.save(commit=False)
                question.task = task
                
                # TODO: Add the other question fields
                question.save() # BUG

            task.title = form.cleaned_data['title']
            task.due_date = form.cleaned_data['due_date']
            task.due_time = form.cleaned_data['due_time']
            task.group = Group.objects.get(name=form.cleaned_data['group'])
            print(task.title)
            # task.save()
            # task = Task.objects.create(
            #     title=form.cleaned_data.get('message'),
            #     topic=topic,
            #     created_by=user
            # )
            return redirect('surveyor_dashboard', pk=user.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTaskForm()

    return render(request, 'surveyor_new_task.html', {'user' : user, 'groups' : groups, 'taskform': form, 'formset': formset})
    # return render(request, 'surveyor_new_task.html')

def new_group(request, pk):
    data = dict()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = GroupForm()

    context = {'form': form, 'pk' : pk}
    data['html_form'] = render_to_string('partial_new_group.html',
        context,
        request=request
    )
    return JsonResponse(data)