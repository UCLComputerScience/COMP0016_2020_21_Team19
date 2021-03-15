import os
import datetime
import pytz
from sys import exit
from collections import namedtuple

import django
from django.contrib.auth import get_user_model
from django.core import management

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

from ActivityLeague.settings import DATABASES
from core.models import Group, Task, Question
from surveyor.models import Surveyor, GroupSurveyor, Organisation
from respondent.models import Respondent, GroupRespondent, Response


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ActivityLeague.settings')
Name = namedtuple("Name", ["first", "last"])


def run_migrations():
    management.call_command("makemigrations", "core", "authentication", "surveyor", "respondent")
    management.call_command("migrate")
    os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD', 'activityleague')

    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        management.call_command("createsuperuser", "--noinput", "--username=admin")


def get_respondent_names():
    return [Name("john", "doe"),
            Name("jack", "white"),
            Name("jean", "brunton"),
            Name("isabelle", "chandler"),
            Name("alisha", "hamilton"),
            Name("oliver", "archer"),
            Name("imogen", "clayton"),
            Name("brandon", "norris"),
            Name("rebecca", "power"),
            Name("luca", "white"),
            Name("sebastian", "howarth"),
            Name("tom", "knight"),
            Name("susie", "gilbert"),
            Name("adam", "prince"),
            Name("julia", "novikov"),
            Name("sam", "duncan")]


def get_surveyor_names():
    return [Name("christine", "black"),
            Name("reece", "gilbert"),
            Name("ben", "connolly")]


def get_group_names():
    return ["COPD Therapy",
            "Hip Therapy",
            "Shoulder Therapy",
            "Diabetics",
            "Post Back Surgery",
            "Elderly"]

"""

Task: Active COPD Rehab
Group: COPD Rehab

Question 1: Take a relaxed, 20 minute walk outside. Rate the following statement afterward: I feel breathless.
response type: likert_desc

Question 2: The NHS recommends breathing exercises found on the link below to support living with COPD. Rate the usefulness of the information.
link: https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/
response_type: numerical_asc

Question 3: Use a few words to describe what is useful about this resource.
link: https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/
response_type: text_positive

Question 4: Use a few words to describe what isn't useful about this resource.
link: https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/
response_type: Text negative

Question 5: The NHS believe that the inhalation of strong-smelling substances like perfumes cause breathlessness. Rate your agreement with this belief.
response_type: likert_asc

Question 6: Briefly describe how you felt after your walk.
response_type: text_neutral

Question 7: Is there anything you've discovered that personally makes living with COPD easier?
response_type: text_positive

"""

def get_tasks():
    return {"COPD Therapy": [{
                                'title': 'Active COPD Rehab',
                                'questions': [
                                    {
                                        'description': 'Take a relaxed, 20 minute walk outside. Rate the following statement afterward: I feel breathless.',
                                        'link': None,
                                        'response_type': Question.ResponseType.LIKERT_DESC
                                    },
                                    {
                                        'description': 'The NHS recommends breathing exercises found on the link below to support living with COPD. Rate the usefulness of the information.',
                                        'link': 'https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/',
                                        'response_type': Question.ResponseType.NUMERICAL_ASC
                                    },
                                    {
                                        'description': 'What is useful about this resource?',
                                        'link': 'https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/',
                                        'response_type': Question.ResponseType.TEXT_POSITIVE
                                    },
                                    {
                                        'description': 'What is not useful about this resource?',
                                        'link': 'https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/living-with/',
                                        'response_type': Question.ResponseType.TEXT_NEGATIVE
                                    },
                                    {
                                        'description': "Is there anything you've discovered that personally makes living with COPD easier?",
                                        'link': None,
                                        'response_type': Question.ResponseType.TEXT_POSITIVE
                                    }
                                ] 
                            }]

# question = models.ForeignKey(Question, on_delete=models.CASCADE)
# respondent = models.ForeignKey(Respondent, on_delete=models.SET_NULL, null=True)
# value = models.FloatField(null=True)
# text = models.CharField(max_length=30, null=True)
# text_positive = models.BooleanField(null=True, default=None)
# date_time = models.DateTimeField()
# link_clicked = models.BooleanField(default=False)

def get_responses_to_COPD():
    return {
        'COPD Therapy': {
            'Active COPD Rehab': {
                'Responses': [{
                    'value': 4,
                    'text': None, 
                    'text_positive': None,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                },
                {
                    'value': 2,
                    'text': None, 
                    'text_positive': None,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': True
                },
                {
                    'value': 'Reference to smoking',
                    'text': None, 
                    'text_positive': None,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                },
                {
                    'value': None,
                    'text': 'Missing social aspect', 
                    'text_positive': True,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                },
                {
                    'value': 5,
                    'text': None, 
                    'text_positive': True,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                },
                {
                    'value': None,
                    'text': 'Tired', 
                    'text_positive': False,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                },
                {
                    'value': 5,
                    'text': None, 
                    'text_positive': True,
                    'date_time': datetime.datetime(2021,2,19,12,30),
                    'link_clicked': False
                }
            }
        }
    }

def create_responses(tasks, respondents):
    for task in tasks:
        for question in task['questions']:
            for respondent in respondents:
                
                Response.objects.create()
    
def insert_dummy_data():
    User = get_user_model()

    organisation = Organisation.objects.create(name="NHS Clinic")

    respondent_users = {}
    respondents = {}

    for name in get_respondent_names():
        fullname = name.first + " " + name.last
        email = name.first + "@" name.last + ".com"
        user = User.objects.create_user(username=name.first, first_name=name.first.capitalize(), last_name=name.last.capitalize(), email=email, password="activityleague")
        respondent_users[fullname] = user
        respondents[fullname] = Respondent.objects.create(user=user, firstname=name.first.capitalize(), surname=name.last.capitalize())
    
    surveyor_users = {}
    surveyors = {}
    
    for name in get_surveyor_names():
        fullname = name.first + " " + name.last
        email = name.first + "@" name.last + ".com"
        user = User.objects.create_user(username=name.first, first_name=name.first.capitalize(), last_name=name.last.capitalize(), email=email, password="activityleague")
        surveyor_users[fullname] = user
        surveyors[fullname] = Surveyor.objects.create(user=user, firstname=name.first.capitalize(), surname=name.last.capitalize(), organisation=organisation)
    

    organisation.admin = surveyors['christine black']
    organisation.save()

    

    # ##################################

    shoulder_1 = Group.objects.create(name="Shoulder Therapy 1")
    hip_1 = Group.objects.create(name="Hip Therapy 1")

    john_doe_grouprespondent_shoulder = GroupRespondent.objects.create(respondent=john_doe, group=shoulder_1)
    john_doe_grouprespondent_hip = GroupRespondent.objects.create(respondent=john_doe, group=hip_1)

    jack_white_grouprespondent_shoulder = GroupRespondent.objects.create(respondent=jack_white, group=shoulder_1)
    jack_white_grouprespondent_hip = GroupRespondent.objects.create(respondent=jack_white, group=hip_1)

    jane_doe_groupsurveyor = GroupSurveyor.objects.create(surveyor=jane_doe, group=shoulder_1)
    christine_black_groupsurveyor = GroupSurveyor.objects.create(surveyor=christine_black, group=hip_1)

    press_ups = Task.objects.create(title="Perform 20 Press-Ups", group=shoulder_1, due_date=datetime.datetime(2021, 7, 1), due_time=datetime.time(10, 0))

    sit_ups = Task.objects.create(title="Perform 20 Sit-Ups", group=hip_1, due_date=datetime.datetime(2021, 7, 1), due_time=datetime.time(10, 0))

    questions = []
    for number in [10, 20, 30]:
        questions.append(Question.objects.create(task=press_ups, link="https://www.url.com", description="How hard was doing " + str(number) + " push-ups?", response_type=Question.ResponseType.LIKERT_ASC))

    for respondent in [john_doe, jack_white]:
        for i, question in enumerate(questions):
            Response.objects.create(question=question, respondent=respondent, value=(i // 3) + 1,  date_time=datetime.datetime(2020, 1, (i // 3) + 1, 10 + (i // 3) + 1, 0, tzinfo=pytz.UTC))
    
    questions = []
    for number in [10, 20, 30]:
        questions.append(Question.objects.create(task=sit_ups, link="https://www.url.com", description="Perform " + str(number) + " Sit-Ups", response_type=1))

    for respondent in [john_doe, jack_white]:
        for i, question in enumerate(questions):
            Response.objects.create(question=question, respondent=respondent, value=(i // 3) + 1,  date_time=datetime.datetime(2020, 1, (i // 3) + 1, 10 + (i // 3) + 1, 0, tzinfo=pytz.UTC))


if __name__ == '__main__':
    django.setup()

    print("Asking django to run migrations")
    run_migrations()
    
    print("Inserting dummy data")
    insert_dummy_data()