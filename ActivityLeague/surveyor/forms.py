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

class SurveyorSignupForm(SignupForm):
    firstname = forms.CharField(max_length=30, min_length=1,  widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    surname = forms.CharField(max_length=30, min_length=1,  widget=forms.TextInput(attrs={'placeholder': 'Surname'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = ""
        self.fields['firstname'].label = ""
        self.fields['surname'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

    def save(self, request):
        user = super(SurveyorSignupForm, self).save(request)

        surveyor = Surveyor(
            user = user,
            firstname=self.cleaned_data.get('firstname'),
            surname=self.cleaned_data.get('surname')
        )

        surveyor.save()

        # Return the django-allauth User instance, 
        # otherwise we will get an error.
        return surveyor.user

class NewLoginForm(LoginForm):
    class Meta:
        field_order = ['login', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""
        # self.fields["forgot"].class
    
    def login(self, *args, **kwargs):
        return super(NewLoginForm, self).login(*args, **kwargs)
    