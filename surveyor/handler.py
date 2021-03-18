import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from tablib import Dataset

from .handler import *
from surveyor.utils import *
from .forms import *


"""
Contains functions designated to handle specific requests made to the views.
"""


def get_new_task(groups, request, user):
    """
    Handles GET requests made to the new_task view.

    :param groups: A ``QuerySet`` of ``Group``\s that are managed by `user`.
    :type groups: django.models.db.QuerySet
    :param request: The GET request sent to new_task.
    :type request: django.http.HttpRequest
    :param user: The ``Surveyor`` representing the currently logged-in user.
    :type user: ``Surveyor``
    :return: The data required by the new_task view to render. Contains: the ``Surveyor``
             object representing the current user, the ``Group``\s that they manage, the
             `taskform` and `formset` required to display the new_task page and any pre-defined
             templates that have been selected, and the `templates` that they can choose from.
    :rtype: dict
    """
    template_id = request.GET.get('template')
    form = TaskForm(request.GET or None, request=request)
    if template_id:  # Load a specific template
        formset = _get_template(template_id)
    else:  # Don't load a template, just render the page
        QuestionFormset = get_question_formset()
        formset = QuestionFormset(queryset=Question.objects.none())
    templates = TaskTemplate.objects.filter(surveyor=user)
    return {'user': user, 'groups': groups, 'taskform': form, 'formset': formset, 'templates': templates}


def _get_template(template_id):
    """
    Retrieves a formset representing a task template for the task with ID `template_id`.

    :param template_id: String representation of the UUID of the ``Template`` to load.
    :type template_id: str
    :return: Form and Formset representing a task template for the task with ID `template_id`.
    :rtype: ``TaskForm`` and django.forms.formsets.BaseFormSet
    """
    template = TaskTemplate.objects.get(id=template_id)
    questions = QuestionTemplate.objects.filter(template=template)
    initial = []
    for question in questions:
        initial.append({
            'description': question.description,
            'link': question.link,
            'response_type': question.response_type
        })
    Formset = get_question_formset(len(initial))
    return Formset(queryset=Question.objects.none(), initial=initial)


def post_organisation(request, user):
    """
    Handles POST requests made to the organisation view.

    :param request: Request made to `organisation`.
    :type request: django.http.HttpRequest
    :param user: The ``Surveyor`` representing the currently logged-in user.
    :type user: ``Surveyor``
    :return: A redirect back to the organisation page.
    :rtype: django.http.HttpResponseRedirect
    """
    if request.POST.get('request_type') == 'delete_surveyor':
        _delete_surveyor(request)

    elif request.POST.get('request_type') == 'invite':  # Inviting a Surveyor
        _invite_surveyor(request, user)

    elif request.POST.get('request_type') == 'import':  # Add multiple Surveyors
        _invite_multiple_surveyors(request, user)

    return HttpResponseRedirect(reverse("organisation"))


def _invite_multiple_surveyors(request, user):
    """
    Invites multiple surveyors to an ``Organisation`` through a spreadsheet of emails.

    Attached to the request is a `file` property containing a formatted spreadsheet (xlsx) of
    emails to send invites out to.

    :param request: The request given to the `organisation` view.
    :type request: django.http.HttpRequest
    :param user: The ``Surveyor`` representing the currently logged-in user.
    :type user: ``Surveyor``
    """
    dataset = Dataset()
    new_persons = request.FILES['file']
    imported_data = dataset.load(new_persons.read(), format='xlsx', headers=False)
    for entry in imported_data:
        if entry[0]:
            try:
                validate_email(entry[0])
            except ValidationError:
                raise Http404("Something was wrong with your file!")
            invite = UserInvitation.create(
                str(entry[0]),
                inviter=request.user,
                organisation=user.organisation,
                is_respondent=False
            )
            invite.send_invitation(request)


def _invite_surveyor(request, user):
    """
    Invite a single new ``Surveyor`` to an ``Organisation`` via email.
    Surveyors cannot be a member of more than one Organisation, so if their
    email already exists in the system they cannot be invited to another Organisation.

    :param request: The request given to the `organisation` view.
    :type request: django.http.HttpRequest
    :param user: The ``Surveyor`` representing the currently logged-in user.
    :type user: ``Surveyor``
    """
    email = request.POST.get('email')

    if not User.objects.filter(email=email).exists():
        invite = UserInvitation.create(
            email,
            inviter=request.user,
            organisation=user.organisation,
            is_respondent=False
        )
        invite.send_invitation(request)


def _delete_surveyor(request):
    """
    Delete the ``Surveyor`` specified in `request`. Only the admin (creator) of an
    ``Organisation`` may perform this operation.

    :param request: The POST request sent to the `organisation` view.
    :type request: django.http.HttpRequest
    """
    surveyor_id = request.POST.get('surveyor')
    surveyor = Surveyor.objects.get(id=surveyor_id)
    surveyor.user.delete()


def _submit_task(form, formset):
    """
    Submits a new task (creates a ``Task`` in the background).

    :param form: The original form containing the metadata
                 of the form, including the ``Group`` that it was assigned to,
                 the due_date of the ``Task`` and the title of it submitted by
                 the ``Surveyor``.
    :type form: ``TaskForm``
    :param formset: The set of questions contained by the new ``Task``.
    :type formset: ``QuestionFormset``
    :return: Redirect to the dashboard page.
    :rtype: django.http.HttpResponseRedirect
    """
    if form.is_valid() and formset.is_valid():
        task = form.save(commit=False)
        task.save()
        questions = formset.save(commit=False)

        # Removing all deleted objects from the form (e.g. deleted additional 
        # questions).
        for deleted in formset.deleted_objects:
            deleted.delete()
        for question_form in questions:
            question_form.link = sanitize_link(question_form.link)
            question_form.task = task
            question_form.save()

        return HttpResponseRedirect(reverse('dashboard'))
    
    else:
        raise Http404("Something was wrong with your task!")


def _save_template(form, formset, user):
    """
    Saves a new template created by the `user`.

    :param form: The original form submitted by `user`.
    :type form: ``TaskForm``
    :param formset: The set of questions in the new template.
    :type formset: ``QuestionFormset``
    :param user: A ``Surveyor`` representing the currently-logged in user.
    :type user: ``Surveyor``
    :return: Redirect to the new-task page.
    :rtype: django.http.HttpResponseRedirect
    """
    form.fields['group'].required = False
    form.fields['due_date'].required = False
    form.fields['due_time'].required = False

    if form.is_valid() and formset.is_valid():
        form.save(commit=False)
        task_template = TaskTemplate.objects.create(name=form.cleaned_data['title'], surveyor=user)
        questions = formset.save(commit=False)
        for deleted in formset.deleted_objects:
            deleted.delete()
        for question_form in questions:
            QuestionTemplate.objects.create(template=task_template,
                                            description=question_form.description,
                                            link=sanitize_link(question_form.link),
                                            response_type=question_form.response_type)
        return HttpResponseRedirect(reverse('new-task') + '?template=' + str(task_template.id))
    else:
        raise Http404("Something was wrong with your template!")


def post_new_task(request, user):
    """
    Handles POST requests sent to the `new_task` view.

    :param request: The POST request sent to the `new_task` view.
    :type request: django.http.HttpRequest
    :param user: A ``Surveyor`` representing the currently logged-in user.
    :type user: ``Surveyor``
    :return: A redirect to either the new-task page (if the `user` has just saved
             a new template or deleted a template) or the dashboard page (if the 
             `user` has just submitted a new task).
    :rtype: django.http.HttpResponseRedirect
    """
    if request.POST.get('delete'): # delete a template
        return _delete_template(request)

    form = TaskForm(request.POST, request=None)
    QuestionFormset = get_question_formset()
    formset = QuestionFormset(request.POST)

    if request.POST.get('save'):  # saving template
        return _save_template(form, formset, user)

    else: # submit a task
        return _submit_task(form, formset)


def post_task_overview(request):
    """
    Handles POST requests sent to the `task_overview` view.

    :param request: The POST request sent to the `task_overview` view.
    :type request: django.http.HttpRequest
    :return: Redirect to the `dashboard` if a task was deleted. Otherwise,
             a redirect to the `task overview` view.
    :rtype: django.http.HttpResponseRedirect
    """
    task_id = request.POST.get('task')
    task = Task.objects.get(id=task_id)
    if request.POST.get('request') == 'complete':
        task.mark_as_complete()
    elif request.POST.get('request') == 'incomplete':
        task.mark_as_incomplete()
    elif request.POST.get('request') == 'delete':
        task.delete()
        return HttpResponseRedirect(reverse("dashboard"))
    return HttpResponseRedirect(reverse("task_overview", args=(task_id,)))


def post_groups(request):
    """
    Handles POST requests to the `groups` view.

    :param request: The POST request sent to the `groups` view.
    :type request: django.http.HttpRequest
    :return: Redirect to the `groups` page.
    :rtype: django.http.HttpResponseRedirect
    """
    if request.POST.get('request_type') == 'new_group':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            gs = GroupSurveyor.objects.create(group=group, surveyor=Surveyor.objects.get(user=request.user))
        else:
            raise Http404("Something went wrong!")
    if request.POST.get('request_type') == 'delete_group':
        group_id = request.POST.get('group')
        group = Group.objects.filter(id=group_id).delete()
    return HttpResponseRedirect(reverse("groups"))


def post_manage_group(request, group_id):
    """
    Handles POST requests to the `manage_group` view.

    :param request: The POST request sent to the `manage_group` view.
    :type request: django.http.HttpRequest
    :param group_id: String representation of the UUID of the ``Group``.
    :type group_id: str
    :return: Redirect to the `manage_group` page.
    :rtype: django.http.HttpResponseRedirect
    """
    group = Group.objects.get(id=group_id)
    # Deleting a participant
    if request.POST.get('request_type') == 'delete_participant':
        _delete_respondent_from_group(group, request)
    # Inviting a participant
    elif request.POST.get('request_type') == 'invite':
        _invite_respondent(group, request)
    # Add multiple participants
    elif request.POST.get('request_type') == 'import':
        _invite_multiple_respondents(group, request)
    # Adding a participant
    else:
        _add_respondent_to_group(group, request)
    return HttpResponseRedirect(reverse("manage-group", args=(group_id,)))


def _add_respondent_to_group(group, request):
    """
    Add the ``Respondent`` specified in `request` to the given `group`.

    :param group: The ``Group`` to add the ``Respondent`` to.
    :type group: ``Group``
    :param request: The POST request sent to the `manage_group` view.
    :type request: django.http.HttpRequest
    """
    respondent_id = request.POST.get('respondent')
    respondent = Respondent.objects.get(id=respondent_id)
    new_object = GroupRespondent.objects.create(group=group, respondent=respondent)


def _invite_multiple_respondents(group, request):
    """
    Invites multiple ``Respondent``\s given by a ``.xlsx`` file in the POST request to the given group.

    :param group: The group to invite the respondents to.
    :type group: ``Group``
    :param request: The request from which to get the ``.xlsx`` file.
    :type request: django.http.HttpRequest
    """
    dataset = Dataset()
    new_persons = request.FILES['file']
    imported_data = dataset.load(new_persons.read(), format='xlsx', headers=False)
    for entry in imported_data:
        if entry[0]:
            try:
                validate_email(entry[0]) # Check the email is valid
            except ValidationError:
                raise Http404("Something was wrong with your file!")
            invite = UserInvitation.create(
                str(entry[0]),
                inviter=request.user,
                group=group,
                is_respondent=True
            )
            invite.send_invitation(request)


def _invite_respondent(group, request):
    """
    Invites the respondent given by the POST request to the given group.
    A ``UserInvitation`` is sent to the email specified in the POST request.

    :param group: The group to invite the respondent to.
    :type group: ``Group``
    :param request: The POST request from which to get the respondent.
    :type request: django.http.HttpRequest
    """
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if Respondent.objects.filter(user=user).exists():
            respondent = Respondent.objects.get(user=user)
            GroupRespondent.objects.create(
                group=group,
                respondent=respondent
            )
        else:
            raise Http404("You cannot invite a Surveyor to a Group!")
    else:
        invite = UserInvitation.create(
            email,
            inviter=request.user,
            group=group,
            is_respondent=True
        )
        invite.send_invitation(request)


def _delete_respondent_from_group(group, request):
    """
    Deletes the respondent given by the POST request from the given group.

    :param group: The group to delete the respondent from.
    :type group: ``Group``
    :param request: The request from which to get the respondent.
    :type request: django.http.HttpRequest
    """
    respondent_id = request.POST.get('respondent')
    respondent = Respondent.objects.get(id=respondent_id)
    GroupRespondent.objects.filter(respondent=respondent, group=group).delete()


def _delete_template(request):
    """
    Deletes the ``TaskTemplate`` specified in the the POST request.

    :param request: The request from which to get the template.
    :type request: django.http.HttpRequest
    :return: Redirect to the 'new task' page.
    :rtype: django.http.HttpResponseRedirect
    """
    template_id = request.POST.get('template')
    TaskTemplate.objects.get(id=template_id).delete()
    return HttpResponseRedirect(reverse('new-task'))
