import os
import datetime
import pytz
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ActivityLeague.settings')

from collections import namedtuple

import django
from django.contrib.auth import get_user_model
from django.core import management
from ActivityLeague.settings import DATABASES

from sys import exit

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


Name = namedtuple("Name", ["first", "last"])


def run_migrations():
    management.call_command("makemigrations", "core", "authentication", "surveyor", "respondent")
    management.call_command("migrate")
    os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD', 'activityleague')

    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        management.call_command("createsuperuser", "--noinput", "--email=email@example.com", "--username=admin")


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
            Name("sam", "duncan"),
            Name("felix", "jones"),
            Name("bruce", "wayne")]


def get_surveyor_names():
    return [Name("christine", "black"),
            Name("reece", "gilbert"),
            Name("ben", "connolly")]


def get_group_names():
    return ["COPD Therapy",
            "Hip Therapy",
            "Shoulder Therapy",
            "Elderly",
            "Diabetics",
            "Post Back Surgery"]

assert(len(get_respondent_names()) % len(get_group_names()) == 0)
assert(len(get_group_names()) % len(get_surveyor_names()) == 0)


def get_tasks():
    return {"COPD Therapy": [{
                            'title': 'Active COPD Rehab',
                            'questions': [
                                    {
                                        'description': 'Take a relaxed, 20 minute walk outside. Rate the following statement afterward: I feel breathless.',
                                        'link': '',
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
                                        'link': '',
                                        'response_type': Question.ResponseType.TEXT_POSITIVE
                                    }
                                ],
                            'due_date': datetime.date(2021, 2, 14),
                            'due_time': datetime.time(12, 0)
                            },
                            {
                            'title': 'Passive COPD Rehab',
                            'questions': [
                                    {
                                        'description': 'Quantitative Question 1',
                                        'link': '',
                                        'response_type': Question.ResponseType.LIKERT_DESC
                                    },
                                    {
                                        'description': 'Quantitative Question 2',
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_ASC
                                    },
                                    {
                                        'description': 'Quantitative Question 3',
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_DESC
                                    },
                                    {
                                        'description': 'Quantitative Question 4',
                                        'link': '',
                                        'response_type': Question.ResponseType.TRAFFIC_LIGHT
                                    },
                                    {
                                        'description': "Quantitative Question 5",
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_ASC
                                    }
                                ],
                            'due_date': datetime.date(2021, 2, 27),
                            'due_time': datetime.time(12, 0)
                            },
                            {
                            'title': 'COPD Roflumilast Medication',
                            'questions': [
                                    {
                                        'description': 'Quantitative Question 1',
                                        'link': '',
                                        'response_type': Question.ResponseType.LIKERT_DESC
                                    },
                                    {
                                        'description': 'Quantitative Question 2',
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_ASC
                                    },
                                    {
                                        'description': 'Quantitative Question 3',
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_DESC
                                    },
                                    {
                                        'description': 'Quantitative Question 4',
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_DESC
                                    },
                                    {
                                        'description': "Quantitative Question 5",
                                        'link': '',
                                        'response_type': Question.ResponseType.NUMERICAL_DESC
                                    }
                                ],
                            'due_date': datetime.date(2021, 3, 16),
                            'due_time': datetime.time(12, 0)
                            }]
    }


def create_quantitative_responses(tasks, respondents, respondents_by_group, questions):
    for task in tasks.values():
        respondent_names = respondents_by_group[task.group.name]
        for question in questions[task.title]:
            for name in respondent_names:
                if not question.is_text:
                    Response.objects.create(question=question, respondent=respondents[name], value=random.choice(question.get_values_list()), text=None, text_positive=None, date_time=datetime.datetime.combine(task.due_date-datetime.timedelta(days=random.randint(2, 10)), task.due_time))
    
    
def insert_dummy_data():
    User = get_user_model()

    organisation = Organisation.objects.create(name="NHS Clinic")

    respondent_users = {}
    respondents = {}

    for name in get_respondent_names():
        fullname = name.first + " " + name.last
        email = name.first + "@" + name.last + ".com"
        user = User.objects.create_user(username=name.first, first_name=name.first.capitalize(), last_name=name.last.capitalize(), email=email, password="activityleague")
        respondent_users[fullname] = user
        respondents[fullname] = Respondent.objects.create(user=user, firstname=name.first.capitalize(), surname=name.last.capitalize())
    
    surveyor_users = {}
    surveyors = {}
    
    for name in get_surveyor_names():
        fullname = name.first + " " + name.last
        email = name.first + "@" + name.last + ".com"
        user = User.objects.create_user(username=name.first, first_name=name.first.capitalize(), last_name=name.last.capitalize(), email=email, password="activityleague")
        surveyor_users[fullname] = user
        surveyors[fullname] = Surveyor.objects.create(user=user, firstname=name.first.capitalize(), surname=name.last.capitalize(), organisation=organisation)
    

    organisation.admin = surveyors['christine black']
    organisation.save()

    groups = {}
    for group_name in get_group_names():
        groups[group_name] = Group.objects.create(name=group_name)

    groups_by_surveyor = {'christine black': [groups["COPD Therapy"], groups["Hip Therapy"]],
                          'reece gilbert': [groups["Shoulder Therapy"], groups["Diabetics"]],
                          'ben connolly': [groups["Post Back Surgery"], groups["Elderly"]]}
    for surveyor, group_list in groups_by_surveyor.items():
        for group in group_list:
            GroupSurveyor.objects.create(surveyor=surveyors[surveyor], group=group)

    groups_by_respondent = {'john doe': [groups["COPD Therapy"], groups["Hip Therapy"], groups["Shoulder Therapy"]],
                            'jack white': [groups["COPD Therapy"], groups["Hip Therapy"], groups["Shoulder Therapy"]],
                            'jean brunton': [groups["COPD Therapy"], groups["Hip Therapy"], groups["Shoulder Therapy"]],
                            'isabelle chandler': [groups["COPD Therapy"], groups["Hip Therapy"], groups["Shoulder Therapy"]]}
    for respondent, group_list in groups_by_respondent.items():
        for group in group_list:
            GroupRespondent.objects.create(respondent=respondents[respondent], group=group)
    
    respondents_by_group = {"COPD Therapy": ['john doe', 'jack white', 'jean brunton', 'isabelle chandler'],
                            "Hip Therapy": ['john doe', 'jack white', 'jean brunton', 'isabelle chandler'],
                            "Shoulder Therapy": ['john doe', 'jack white', 'jean brunton', 'isabelle chandler']}

    tasks = {}
    questions = {}
    for group_name, task_list in get_tasks().items():
        group = groups[group_name]
        for task in task_list:
            tasks[group_name] = Task.objects.create(title=task['title'], group=group, due_date=task['due_date'], due_time=task['due_time'])

            questions[task['title']] = []
            for question in task['questions']:
                print('Description: ', question['description'])
                print('Link:', question['link'])
                questions[task['title']].append(Question.objects.create(task=tasks[group_name], link=question['link'], description=question['description'], response_type=question['response_type']))

    create_quantitative_responses(tasks, respondents, respondents_by_group, questions)

if __name__ == '__main__':
    django.setup()

    print("Asking django to run migrations")
    run_migrations()
    
    print("Inserting dummy data")
    from core.models import Group, Task, Question
    from surveyor.models import Surveyor, GroupSurveyor, Organisation
    from respondent.models import Respondent, GroupRespondent, Response
    insert_dummy_data()