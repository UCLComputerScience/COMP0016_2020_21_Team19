import datetime
import pytz

from respondent.models import Respondent, Response
from surveyor.models import Surveyor, Question, Task, Group, GroupSurveyor
from surveyor import views
from core.utils import get_tasks
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


class TaskOverViewTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))
        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_response_code_200_if_valid(self):  
        request = self.factory.get('/task/')
        request.user = self.user
        response = views.task_overview(request, self.task.id)
        self.assertEqual(response.status_code, 200)    


class DashboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)

    def test_dashboard_renders_on_login(self):
        request = self.factory.get('/dashboard')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.dashboard(request)
        self.assertEqual(response.status_code, 200)


class LeaderboardTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
    
    def test_leaderboard_renders_on_login(self):
        request = self.factory.get('/leaderboard')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.leaderboard(request)
        self.assertEqual(response.status_code, 200)


class NewTaskTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_new_task_renders(self):
        request = self.factory.get('/new_task')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_task(request)
        self.assertEqual(response.status_code, 200)


class GetQuestionsTestCase(TestCase):
   
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.surveyor_user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.surveyor_user, firstname='Jane', surname='White')
        self.respondent_user = User.objects.create_user(username='Emma', email='emma@email.com', password='activityleague')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='Emma', surname='Green')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)

        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))

        self.question_1 = Question.objects.create(task=self.task, description="Walk for 2 miles", response_type=1)
        self.question_2 = Question.objects.create(task=self.task, description="Socialise with 2 people today", response_type=2)
        self.question_3 = Question.objects.create(task=self.task, description="Spend less than 1h per day on your phone", response_type=3)

        self.response_1 = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, text=None, date_time=datetime.datetime.now(tz=pytz.UTC), link_clicked=True)
        self.response_2 = Response.objects.create(question=self.question_2, respondent=self.respondent, value=1, text=None, date_time=datetime.datetime.now(tz=pytz.UTC), link_clicked=True)
        self.response_3 = Response.objects.create(question=self.question_3, respondent=self.respondent, value=None, text='Hard', date_time=datetime.datetime.now(tz=pytz.UTC), link_clicked=True)


    def test_data_formatted_appropriately(self):
        data = views.get_questions(self.task.id)
        self.assertTrue(data)
        entry = data[0]
        self.assertEqual(entry.keys(), {'id', 'link', 'type', 'description', 'link_clicks', 'pie_chart_labels', 'pie_chart_data', 'word_cloud'})
    
    def test_chart_likert_labels_correct(self):
        data = views.get_questions(self.task.id)
        likert_entry = None
        for entry in data:
            if entry['id'] == self.question_1.id:
                likert_entry = entry
        self.assertEqual(likert_entry['pie_chart_labels'], ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])

    def test_chart_traffic_labels_correct(self):
        data = views.get_questions(self.task.id)
        traffic_entry = None
        for entry in data:
            if entry['id'] == self.question_2.id:
                traffic_entry = entry
        self.assertEqual(traffic_entry['pie_chart_labels'], ['Red', 'Yellow', 'Green'])
    
    def test_chart_data_correct(self):
        pass
    
    def test_text_responses_correct(self):
        pass
    
    def test_link_clicks_correct(self):
        data = views.get_questions(self.task.id)
        clicks = []
        for i in range(0, 3):
            clicks.append(1 if data[i]['link_clicks'] else 0)
        self.assertEqual(clicks, [1, 1, 1])

    def test_question_descriptions_correct(self):
        data = views.get_questions(self.task.id)
        descriptions = {entry['description'] for entry in data}
        self.assertEqual(descriptions, {"Walk for 2 miles", "Socialise with 2 people today", "Spend less than 1h per day on your phone"})
        

class NewGroupTestCase(TestCase):
    """
    This is going to be 
    """
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_new_group_renders(self):
        request = self.factory.get('/groups')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.new_group(request)
        self.assertEqual(response.status_code, 200)


class GroupsTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
        self.task = Task.objects.create(title="Perform 20 Press-Ups", group=self.group, due_date=datetime.datetime(2021, 7, 3, tzinfo=pytz.UTC), due_time=datetime.time(10, 0))

        self.question = Question.objects.create(task=self.task, description="This task was difficult", response_type=1)
    
    def test_groups_page_renders_on_login(self):
        request = self.factory.get('/groups')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.groups(request)
        self.assertEqual(response.status_code, 200)


class ManageGroupTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
    
    def test_manage_groups_renders(self):
        request = self.factory.get('/manage_group/')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.manage_group(request, self.group.id)
        self.assertEqual(response.status_code, 200)


class AddUserTestCase(TestCase):
    """
    This returns a JSON response so can be tested more thoroughly
    """
    pass

