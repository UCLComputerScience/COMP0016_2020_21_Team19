import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from surveyor.models import Surveyor, Group, GroupSurveyor, Task, Question

class SurveyorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="mrtest", email="mrtest@gmail.com", password="activityleague")
        Surveyor.objects.create(user=user, firstname="Mr", surname="Test")

    def test_firstname_label(self):
        """
        Tests that the firstname field of the object created is "firstname".
        """
        test_user = Surveyor.objects.get(firstname="Mr", surname="Test")
        firstname_label = test_user._meta.get_field('firstname').verbose_name
        self.assertEqual(firstname_label, 'firstname')
    
    def test_surname_label(self):
        """
        Tests the surname field of Surveyor is "surname".
        """
        test_user = Surveyor.objects.get(firstname="Mr", surname="Test")
        surname_label = test_user._meta.get_field('surname').verbose_name
        self.assertEqual(surname_label, 'surname')

    def test_firstname_max_length_is_30(self):
        test_user = Surveyor.objects.get(firstname="Mr", surname="Test")
        max_length = test_user._meta.get_field('firstname').max_length
        self.assertEqual(max_length, 30)

    def test_surname_max_length_is_30(self):
        test_user = Surveyor.objects.get(firstname="Mr", surname="Test")
        max_length = test_user._meta.get_field('surname').max_length
        self.assertEqual(max_length, 30)
    
    def test_surveyor_name_is_correct(self):
        """
        Tests str(surveyor) is surveyor.firstname + " " + surveyor.surname
        """
        test_user = Surveyor.objects.get(firstname="Mr", surname="Test")
        name = "Mr Test"
        self.assertEqual(str(test_user), name)
    

class GroupTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name="Test Group")
    
    def test_name_label(self):
        """
        There should be a field 'name' on Group objects.
        """
        label = Group.objects.get(name="Test Group")._meta.get_field('name').verbose_name
        self.assertEqual(label, 'name')
    
    def test_group_name(self):
        """
        Group names should be returned correctly.
        """
        group = Group.objects.get(name="Test Group")
        name = str(group)
        self.assertEqual(name, 'Test Group')


class GroupSurveyorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="mrtest", email="mrtest@gmail.com", password="activityleague")
        surveyor = Surveyor.objects.create(user=user, firstname="Mr", surname="Test")
        group = Group.objects.create(name="Test Group")
        GroupSurveyor.objects.create(group=group,surveyor=surveyor)

    def test_surveyor_label(self):
        """
        Surveyor objects should have a field 'surveyor'.
        """
        group = Group.objects.get(name="Test Group")
        surveyor = Surveyor.objects.get(firstname="Mr", surname="Test")
        label = GroupSurveyor.objects.get(group=group, surveyor=surveyor)._meta.get_field('surveyor').verbose_name
        self.assertEqual(label, 'surveyor')

    def test_group_label(self):
        """
        Surveyor objects should have a field 'group'.
        """
        group = Group.objects.get(name="Test Group")
        surveyor = Surveyor.objects.get(firstname="Mr", surname="Test")
        label = GroupSurveyor.objects.get(group=group, surveyor=surveyor)._meta.get_field('group').verbose_name
        self.assertEqual(label, 'group')


class TaskTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        title = "Test Task Title"
        group = Group.objects.create(name="Test Group")
        due_date = datetime.datetime(2021, 7, 3)
        due_time = datetime.time(10, 0)
        task = Task.objects.create(title=title, group=group, due_date=due_date, due_time=due_time)
    
    def test_title_field(self):
        """
        Task objects should have a field 'title'.
        """
        task = Task.objects.get(title="Test Task Title")
        title_label = task._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'title')

    def test_group_field(self):
        """
        Task objects should have a field 'group'.
        """
        task = Task.objects.get(title="Test Task Title")
        group_label = task._meta.get_field('group').verbose_name
        self.assertEqual(group_label, 'group')

    def test_due_date_field(self):
        """
        Task objects should have a field 'due date'.
        """
        task = Task.objects.get(title="Test Task Title")
        due_date_label = task._meta.get_field('due_date').verbose_name
        self.assertEqual(due_date_label, 'due date')

    def test_due_time_field(self):
        """
        Task objects should have a field 'due time'.
        """
        task = Task.objects.get(title="Test Task Title")
        due_time_label = task._meta.get_field('due_time').verbose_name
        self.assertEqual(due_time_label, 'due time')

    def test_name_is_correct(self):
        """
        str(Task) shoud return Task.title.
        """
        task = Task.objects.get(title="Test Task Title")
        self.assertEqual(str(task), "Test Task Title")


class QuestionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        title = "Test Task Title"
        group = Group.objects.create(name="Test Group")
        due_date = datetime.datetime(2021, 7, 3)
        due_time = datetime.time(10, 0)
        task = Task.objects.create(title=title, group=group, due_date=due_date, due_time=due_time)
        link = "www.bbc.com"
        description = "This is a test description"
        response_type = 1
        question = Question.objects.create(task=task, link=link, description=description, response_type=response_type)
    
    def test_task_label(self):
        """
        Question objects should have a field 'task'.
        """
        question = Question.objects.get(description="This is a test description")
        task_label = question._meta.get_field('task').verbose_name
        self.assertEqual(task_label, 'task')

    def test_link_label(self):
        """
        Question objects should have a field 'link'.
        """
        question = Question.objects.get(description="This is a test description")
        link_label = question._meta.get_field('link').verbose_name
        self.assertEqual(link_label, 'link')

    def test_description_label(self):
        """
        Question objects should have a field 'description'.
        """
        question = Question.objects.get(description="This is a test description")
        description_label = question._meta.get_field('description').verbose_name
        self.assertEqual(description_label, 'description')

    def test_response_type_label(self):
        """
        Question objects should have a field 'response type'.
        """
        question = Question.objects.get(description="This is a test description")
        response_type_label = question._meta.get_field('response_type').verbose_name
        self.assertEqual(response_type_label, 'response type')