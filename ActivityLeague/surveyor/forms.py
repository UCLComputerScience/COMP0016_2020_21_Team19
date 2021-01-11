from django import forms
from django.forms import modelformset_factory

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
            'due_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'MM/DD/YYYY'
                }
            ),
            'due_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM'
                }
            )
        }


QuestionFormset = modelformset_factory(
    Question,
    fields=('link', 'description', 'response_type'),
    extra=1,
    widgets={
        'description': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Question here'
            }
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