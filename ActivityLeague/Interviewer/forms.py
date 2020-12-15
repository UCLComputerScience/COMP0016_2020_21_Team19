from django import forms
from django.forms import modelformset_factory

from .models import *

GROUP_CHOICES = Group.objects.all()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'group_id', 'due_date', 'due_time')
        labels = {
            'title': 'Task Title',
            'group_id': 'Group',
            'due_date': 'Date',
            'due_time': 'Time' 
        }
        widgets={
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Task Tile here'
                }
            ),
            'group_id': forms.Select(choices=GROUP_CHOICES),
            'due_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DD/MM/YYYY'
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
    fields=('link', 'description'),
    extra=4,
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
                'placeholder': 'URL (optional)'
            }
        ),
    }
)