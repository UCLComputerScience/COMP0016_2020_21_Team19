from django import forms
from django.forms import modelformset_factory
from allauth.account.forms import SignupForm, LoginForm

from .models import *

GROUP_CHOICES = Group.objects.all()

RESPONSE_TYPES = [(1, 'Likert Scale'), (2, 'Traffic Light'),(3, 'Text Field')]

class TaskForm(forms.ModelForm):
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
            'group': forms.Select(choices=GROUP_CHOICES, attrs={'class' : 'custom-select d-block w-100'}),
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
