import datetime
import pytz

from respondent.models import Respondent, Response, GroupRespondent
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
        """
        Accessing /task/ should give status code of 200. Accessing /task/a where a is an invalid
        UUID should not give you a status code of 404, though we know this behaviour is already defined
        given the internal dependency on the django-core get_object_or_404 method which has already
        been extensively tested.
        """
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

    def test_response_code_200_if_valid_path(self):
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
    
    def test_response_code_200_if_valid_path(self):
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
    
    def test_response_code_200_if_valid_path(self):
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

        self.response_1 = Response.objects.create(question=self.question_1, respondent=self.respondent, value=1, text=None, date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC), link_clicked=True)
        self.response_2 = Response.objects.create(question=self.question_2, respondent=self.respondent, value=1, text=None, date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC), link_clicked=True)
        self.response_3 = Response.objects.create(question=self.question_3, respondent=self.respondent, value=None, text='Hard', date_time=datetime.datetime(2021, 7, 4, 12, 0, tzinfo=pytz.UTC), link_clicked=True)


    def test_data_formatted_appropriately(self):
        """
        Each dictionary in the list data should contain keys: id, link, type, description, link_clicks, pie_chart_labels,
        pie_chart_data, word_cloud.
        """
        data = views.get_questions(self.task.id)
        self.assertTrue(data)
        entry = data[0]
        self.assertEqual(entry.keys(), {'id', 'link', 'type', 'description', 'link_clicks', 'pie_chart_labels', 'pie_chart_data', 'word_cloud'})
    
    def test_chart_likert_labels_correct(self):
        """
        Questions with response_type = 1 (likert questions) should have labels: 'Strongly Disagree', 'Disagree', 'Neutral',
        'Agree', 'Strongly Agree'.
        """
        data = views.get_questions(self.task.id)
        likert_entry = None
        for entry in data:
            if entry['type'] == 'likert':
                likert_entry = entry
                break
        self.assertEqual(likert_entry['pie_chart_labels'], ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'])

    def test_chart_traffic_labels_correct(self):
        """
        Questions with response_type = 2 (traffic light questions) should have labels: 'Red', 'Yellow', 'Green'.
        """
        data = views.get_questions(self.task.id)
        traffic_entry = None
        for entry in data:
            if entry['type'] == 'traffic':
                traffic_entry = entry
                break
        self.assertEqual(traffic_entry['pie_chart_labels'], ['Red', 'Yellow', 'Green'])
    
    def test_word_cloud_url_correct(self):
        """
        If a question contains a text-based response, we should get a link to a generated word cloud image
        of the form 'data:image/png;base64' + string.
        """
        data = views.get_questions(self.task.id)
        text_entry = None
        for entry in data:
            if entry['type'] == 'text':
                text_entry = entry
                break
        self.assertTrue('data:image/png;base64' in text_entry['word_cloud'])
    
    def test_link_clicks_correct(self):
        """
        Tests whether the number of link clicks returned is the same as the number of link clicks recorded
        per question.
        """
        data = views.get_questions(self.task.id)
        clicks = []
        for i in range(0, 3):
            clicks.append(1 if data[i]['link_clicks'] else 0)
        self.assertEqual(clicks, [1, 1, 1])

    def test_question_descriptions_correct(self):
        """
        Tests whether the descriptions to each of the questions returned are correct: we do not return
        any descriptions of questions that are not part of the task and do not neglect any descriptions
        that are part of the task.
        """
        data = views.get_questions(self.task.id)
        descriptions = {entry['description'] for entry in data}
        self.assertEqual(descriptions, {"Walk for 2 miles", "Socialise with 2 people today", "Spend less than 1h per day on your phone"})
        

class NewGroupTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jane', email='jane@email.com', password='activityleague')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Jane', surname='White')
    
    def test_response_code_200_if_valid_path(self):
        self.client.login(username='jane', password='activityleague')
        request = self.factory.get('/new_group')
        request.user = self.user
        response = views.new_group(request)
        self.assertEqual(response.status_code, 200)
    
    def test_new_group_post(self):
        self.client.login(username='jane', password='activityleague')
        request = self.client.post('/new_group', {'name': 'Shoulder Therapy 1'})
        self.assertTrue(Group.objects.filter(name="Shoulder Therapy 1").exists())
        group = Group.objects.get(name="Shoulder Therapy 1")
        self.assertTrue(GroupSurveyor.objects.filter(surveyor=self.surveyor, group=group).exists())


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
    
    def test_response_code_200_if_valid_login(self):
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
        self.respondent_user = User.objects.create_user(username='Emma', email='emma@email.com', password='activityleague')
        self.respondent = Respondent.objects.create(user=self.respondent_user, firstname='Emma', surname='Green')
        self.group = Group.objects.create(name="Lung Rehabilitation")
        self.group_surveyor = GroupSurveyor.objects.create(surveyor=self.surveyor, group=self.group)
    
    def test_response_code_200_if_valid(self):
        request = self.factory.get('/manage_group/')
        request.user = self.user
        login = self.client.login(username='jane', password='activityleague')
        response = views.manage_group(request, self.group.id)
        self.assertEqual(response.status_code, 200)

    def test_manage_group_post(self):
        self.client.login(username='jane', password='activityleague')
        request = self.client.post('/manage_group/' + str(self.group.id), {'respondent': self.respondent.id})
        group_respondent = GroupRespondent.objects.get(respondent=self.respondent)
        self.assertEqual(group_respondent.group, self.group)