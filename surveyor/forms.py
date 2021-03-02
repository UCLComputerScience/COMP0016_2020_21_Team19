from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm, LoginForm

from .models import *
from respondent.models import *
from core.models import UserInvitation 


RESPONSE_TYPES = [
    (1, 'Likert Scale'),
    (2, 'Traffic Light'),
    (3, 'Text Field'),
    (4, '1-5 Scale'),
    (5, 'Text (Positive)'),
    (6, 'Text (Negative)')
    ]

class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        if self.request:
            surveyor = Surveyor.objects.get(user=self.request.user)
            group_surveyors = GroupSurveyor.objects.filter(surveyor=surveyor).values_list('group', flat=True)
            self.GROUP_CHOICES = Group.objects.filter(pk__in=group_surveyors)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.request:
            self.fields['group'] = forms.ModelChoiceField(
                queryset=self.GROUP_CHOICES,
                widget=forms.Select(
                    attrs={
                        'class' : 'custom-select d-block w-100'
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
        widgets={
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Task Title here'
                }
            ),
            'due_date': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                # 'id': 'due_date',
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


QuestionFormset = modelformset_factory(
    Question,
    fields=('link', 'description', 'response_type'),
    min_num=0,
    validate_min=True,
    widgets={
        'description': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Question here'
            },
        ),
        'link': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'URL'
            }
        ),
        'response_type': forms.Select(choices=RESPONSE_TYPES, attrs={'class' : 'custom-select d-block w-100'})
    }
)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name': 'Group Name'
        }
        widgets={
            'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Group Name here'
                }
            )
        }

class AddUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.group_pk = kwargs.pop('group_pk')
        group = Group.objects.get(pk=self.group_pk)
        group_respondents_ids = GroupRespondent.objects.filter(group=group).values_list('respondent', flat=True)
        self.USERS = Respondent.objects.exclude(pk__in=group_respondents_ids)
        super(AddUserForm,self).__init__(*args, **kwargs)

        self.fields['respondent'] = forms.ModelChoiceField(
            queryset=self.USERS,
            widget=forms.Select(
                attrs={
                    'id': 'post-respondent',
                    'class' : 'custom-select d-block w-100'
                }
            ),
            label="Select User:"
        )


    class Meta:
        model = GroupRespondent
        fields = ('respondent',)


class InviteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InviteUserForm,self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'placeholder': "Users's Email",
                'class' : 'form-control d-block w-100'
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
    file = forms.FileField()