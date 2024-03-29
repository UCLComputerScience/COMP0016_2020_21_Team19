from django import forms
from django.forms import modelformset_factory

from authentication.models import UserInvitation
from core.models import *
from respondent.models import *
from .models import *

class TaskForm(forms.ModelForm):
    """
    Form used to create new Task instances.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        if self.request:
            surveyor = Surveyor.objects.get(user=self.request.user)
            group_surveyors = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
            self.GROUP_CHOICES = Group.objects.filter(id__in=group_surveyors)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.request:
            self.fields['group'] = forms.ModelChoiceField(
                queryset=self.GROUP_CHOICES,
                widget=forms.Select(
                    attrs={
                        'class': 'custom-select d-block w-100'
                    }
                )
            )

    class Meta:
        model = Task
        fields = ('title', 'group', 'due_date', 'due_time')
        labels = {
            'title': 'Task Title',
            'group': 'Group',
            'due_date': 'Date',
            'due_time': 'Time'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Task Title here'
            }
            ),
            'due_date': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'placeholder': 'MM/DD/YYYY',
                }
            ),
            'due_time': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'class': 'form-control timepicker',
                    'type': 'time',
                    'placeholder': 'HH:MM'
                }
            )
        }


def get_question_formset(extra=1):
    """
    Returns a formset with the specified nummber of `extra` instances of forms.
    One form can be used to create one Question.

    :param extra: defines the number of fields the form should have
                  (i.e.) the number of ``Question``\s to create, defaults to 1.
    :type extra: int, optional
    :return: A ``Question`` formset with the specified number of instances.
    :rtype: django.forms.BaseFormset
    """
    return modelformset_factory(
        Question,
        fields=('link', 'description', 'response_type'),
        min_num=0,
        validate_min=True,
        extra=extra,
        can_delete=True,
        widgets={
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question here',
                    'required': ''
                }
            ),
            'link': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'URL'
                },
            ),
            'response_type': forms.Select(choices=Question.ResponseType.choices, attrs={'class': 'custom-select d-block w-100', 'required': ''})
        }
    )


class GroupForm(forms.ModelForm):
    """
    Form used to create new Group instances.
    """

    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name': 'Group Name'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Group Name here'
                }
            )
        }


class AddUserForm(forms.ModelForm):
    """
    Form used to add ``Respondent``\s to ``Group``\s.
    """

    def __init__(self, *args, **kwargs):
        self.group_id = kwargs.pop('group_id')
        group = Group.objects.get(id=self.group_id)
        group_respondents_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
        self.USERS = Respondent.objects.exclude(id__in=group_respondents_ids)
        super(AddUserForm, self).__init__(*args, **kwargs)

        self.fields['respondent'] = forms.ModelChoiceField(
            queryset=self.USERS,
            widget=forms.Select(
                attrs={
                    'id': 'post-respondent',
                    'class': 'custom-select d-block w-100'
                }
            ),
            label="Select User:"
        )

    class Meta:
        model = GroupRespondent
        fields = ('respondent',)


class InviteSurveyorForm(forms.ModelForm):
    """
    Form used to invite ``Surveyor``\s to ``Organisations``\s.
    """

    def __init__(self, *args, **kwargs):
        super(InviteSurveyorForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'placeholder': " Email",
                'class': 'form-control d-block w-100'
            }),
            error_messages={
                'required': "Please enter the surveyor's email address.",
                'invalid': "Please enter a valid email address."
            },
            label="Enter the surveyor's email:"
        )

    class Meta:
        model = UserInvitation
        fields = ('email',)

class InviteUserForm(forms.ModelForm):
    """
    Form used to invite ``Respondent``\s to ``Group``\s.
    """

    def __init__(self, *args, **kwargs):
        super(InviteUserForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'placeholder': "Users's Email",
                'class': 'form-control d-block w-100'
            }),
            error_messages={
                'required': "Please enter the user's email address.",
                'invalid': "Please enter a valid email address."
            },
            label="Enter the user's email:"
        )

    class Meta:
        model = UserInvitation
        fields = ('email',)


class MultipleUserForm(forms.Form):
    """
    Form used to invite multiple ``Respondent``\s / ``Surveyor``\s 
    to ``Group``\s / ``Organisations``\s.
    """
    file = forms.FileField()
