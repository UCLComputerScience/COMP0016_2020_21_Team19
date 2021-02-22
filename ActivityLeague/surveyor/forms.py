from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm, LoginForm

from .models import *
from respondent.models import *


RESPONSE_TYPES = [(1, 'Likert Scale'), (2, 'Traffic Light'),(3, 'Text Field'), (4, '1-5 Scale')]

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
            # 'group': forms.Select(choices=GROUP_CHOICES, attrs={'class' : 'custom-select d-block w-100'}),
            'due_date': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                'class': 'form-control',
                'type': 'date'
                }
            ),
            'due_time': forms.TimeInput(
                format='%H:%M',
                attrs={
                'class': 'form-control',
                'type': 'time'
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
                )
            )

    class Meta:
        model = GroupRespondent
        fields = ('respondent',)
        labels = {
            'respondent': 'Select User',
        }