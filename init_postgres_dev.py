import os
import datetime
import pytz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ActivityLeague.settings')

from django.contrib.auth import get_user_model
from django.core import management
from ActivityLeague.settings import DATABASES

from sys import exit

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

def run_migrations():
    from django.core import management

    management.call_command("makemigrations", "surveyor", "respondent")
    management.call_command("migrate")
    os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD', 'activityleague')

    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        management.call_command("createsuperuser", "--noinput", "--email=email@example.com", "--username=admin")

def insert_dummy_data():
    from surveyor.models import Surveyor, Group, GroupSurveyor, Task, Question
    from respondent.models import Respondent, GroupRespondent, Response

    User = get_user_model()

    john_doe_user = User.objects.create_user(username="john", email="john@doe.com", password="activityleague")
    jack_white_user = User.objects.create_user(username="jack", email="jack@white.com", password="activityleague")

    jane_doe_user = User.objects.create_user(username="jane", email="jane@doe.com", password="activityleague")
    christine_black_user = User.objects.create_user(username="christine", email="christine@black.com", password="activityleague")

    john_doe = Respondent.objects.create(user=john_doe_user, firstname="John", surname="Doe")
    jack_white = Respondent.objects.create(user=jack_white_user, firstname="Jack", surname="White")

    jane_doe = Surveyor.objects.create(user=jane_doe_user, firstname="Jane", surname="Doe")
    christine_black = Surveyor.objects.create(user=christine_black_user, firstname="Christine", surname="Black")

    shoulder_1 = Group.objects.create(name="Shoulder Therapy 1")
    hip_1 = Group.objects.create(name="Hip Therapy 1")

    john_doe_grouprespondent_shoulder = GroupRespondent.objects.create(respondent=john_doe, group=shoulder_1)
    john_doe_grouprespondent_hip = GroupRespondent.objects.create(respondent=john_doe, group=hip_1)

    jack_white_grouprespondent_shoulder = GroupRespondent.objects.create(respondent=jack_white, group=shoulder_1)
    jack_white_grouprespondent_hip = GroupRespondent.objects.create(respondent=jack_white, group=hip_1)

    jane_doe_groupsurveyor = GroupSurveyor.objects.create(surveyor=jane_doe, group=shoulder_1)
    christine_black_groupsurveyor = GroupSurveyor.objects.create(surveyor=christine_black, group=hip_1)

    press_up_tasks = [Task.objects.create(title="Perform 20 Press-Ups", group=shoulder_1, due_date=datetime.datetime(2021, 7, i), due_time=datetime.time(10 + i, 0)) for i in range(1,4)]

    sit_ups = Task.objects.create(title="Perform 20 Sit-Ups", group=hip_1, due_date=datetime.datetime(2021, 7, 1), due_time=datetime.time(10, 0))

    questions = []
    for task in press_up_tasks:
        for number in [10, 20, 30]:
            questions.append(Question.objects.create(task=task, link="https://www.url.com", description="Do " + str(number) + " Push-Ups", response_type=1))

    for respondent in [john_doe, jack_white]:
        for i, question in enumerate(questions):
            Response.objects.create(question=question, respondent=respondent, value=(i // 3) + 1,  date_time=datetime.datetime(2020, 1, (i // 3) + 1, 10 + (i // 3) + 1, 0, tzinfo=pytz.UTC))
    
    questions = []
    for number in [10, 20, 30]:
        questions.append(Question.objects.create(task=sit_ups, link="https://www.url.com", description="Perform " + str(number) + " Sit-Ups", response_type=1))

    for respondent in [john_doe, jack_white]:
        for i, question in enumerate(questions):
            Response.objects.create(question=question, respondent=respondent, value=(i // 3) + 1,  date_time=datetime.datetime(2020, 1, (i // 3) + 1, 10 + (i // 3) + 1, 0, tzinfo=pytz.UTC))

def main():
    import django
    django.setup()

    print("Asking django to run migrations")
    run_migrations()
    
    print("Inserting dummy data")
    insert_dummy_data()

if __name__ == '__main__':
    main()