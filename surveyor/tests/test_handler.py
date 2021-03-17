import datetime

from django.http import HttpRequest
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError

from surveyor import handler
from surveyor.forms import *
from surveyor.models import *
from respondent.models import *
from core.models import *

def _setUp(testcase):
    testcase.factory = RequestFactory()

    testcase.auth_surveyor = User.objects.create_user('email@email.com', 'activityleague')
    testcase.surveyor = Surveyor.objects.create(firstname="Firstname", surname="Surname", user=testcase.auth_surveyor)
    
    testcase.group_1 = Group.objects.create(name="Group 1")
    testcase.group_2 = Group.objects.create(name="Group 2")

    testcase.group_surveyor_1 = GroupSurveyor.objects.create(surveyor=testcase.surveyor, group=testcase.group_1)
    testcase.group_surveyor_2 = GroupSurveyor.objects.create(surveyor=testcase.surveyor, group=testcase.group_2)

    testcase.task = Task.objects.create(title="Test Task",
                                    group=testcase.group_1,
                                    due_date=datetime.date(2021, 12, 31),
                                    due_time=datetime.time(23, 59))

    testcase.question_1 = Question.objects.create(description="Question 1", response_type=Question.ResponseType.LIKERT_ASC, task=testcase.task)
    testcase.question_2 = Question.objects.create(description="Question 2", response_type=Question.ResponseType.TEXT_NEUTRAL, task=testcase.task)
    testcase.question_3 = Question.objects.create(description="Question 3", response_type=Question.ResponseType.NUMERICAL_DESC, task=testcase.task)

    testcase.task_template = TaskTemplate.objects.create(name="", surveyor=testcase.surveyor)

    testcase.question_template_1 = QuestionTemplate.objects.create(template=testcase.task_template,
                                                                description=testcase.question_1.description,
                                                                response_type=testcase.question_1.response_type)
    
    testcase.question_template_2 = QuestionTemplate.objects.create(template=testcase.task_template,
                                                                description=testcase.question_2.description,
                                                                response_type=testcase.question_2.response_type)

    testcase.question_template_3 = QuestionTemplate.objects.create(template=testcase.task_template,
                                                                description=testcase.question_3.description,
                                                                response_type=testcase.question_3.response_type)
    testcase.client.login(username='email@email.com', password='activityleague')


class GetNewTaskTestCase(TestCase):
    """
    No need to tests groups and user given they are passed in as params
    and not modified in any way.
    """

    def setUp(self):
        _setUp(self)
        

    def test_returns_correct_dict(self):
        request = self.factory.get(reverse('new-task'))
        request.user = self.auth_surveyor
        group_ids = GroupSurveyor.objects.filter(surveyor=self.surveyor).values_list('group', flat=True)
        groups = Group.objects.filter(id__in=group_ids)
        response = handler.get_new_task(groups, request, self.surveyor)
        self.assertEqual(response.keys(), {'user', 'groups', 'taskform', 'formset', 'templates'})


    def test_returns_correct_template_formset_if_specified(self):
        """
        If we specify a template, check that we get the formset for that template
        """
        payload = {'template': self.task_template.id}
        request = self.factory.get(reverse('new-task'), payload)
        request.user = self.auth_surveyor
        group_ids = GroupSurveyor.objects.filter(surveyor=self.surveyor).values_list('group', flat=True)
        groups = Group.objects.filter(id__in=group_ids)
        response = handler.get_new_task(groups, request, self.surveyor)
        formset = response['formset']
        descriptions = [self.question_1.description, self.question_2.description, self.question_3.description]
        self.assertEqual(len(descriptions), len(formset))
        for description, form in zip(descriptions, formset):
            self.assertTrue(description in str(form['description']))


    def test_returns_correct_templates(self):
        """
        Check we get the TaskTemplates that have been created by the Surveyor
        """
        request = self.factory.get(reverse('new-task'))
        request.user = self.auth_surveyor
        group_ids = GroupSurveyor.objects.filter(surveyor=self.surveyor).values_list('group', flat=True)
        groups = Group.objects.filter(id__in=group_ids)
        templates = handler.get_new_task(groups, request, self.surveyor)['templates']
        self.assertTrue(self.task_template in templates and len(templates) == 1)
        

    def test_taskform_fields_correct(self):
        """
        We should have a TaskForm with fields ('title', 'due_date', 'due_time', 'group')
        """
        request = self.factory.get(reverse('new-task'))
        request.user = self.auth_surveyor
        taskform = handler.get_new_task(None, request, None)['taskform']
        self.assertEqual(taskform.fields.keys(), {'title', 'due_date', 'due_time', 'group'})    


class PostOrganisationTestCase(TestCase):

    def setUp(self):
        _setUp(self)
    
    def test_delete_surveyor(self):
        payload = {'request_type': 'delete_surveyor', 'surveyor': self.surveyor.id}
        request = self.factory.post(reverse('organisation'), payload)
        handler.post_organisation(request, self.surveyor)
        self.assertFalse(Surveyor.objects.filter(firstname="Firstname").exists())

    def test_invite_surveyor(self):
        payload = {'request_type': 'invite', 'email': 'mail@mail.com'}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.auth_surveyor
        handler.post_organisation(request, self.surveyor)
        self.assertTrue(UserInvitation.objects.filter(email='mail@mail.com').exists())

    def test_invite_multiple_surveyors(self):
        pass


class PostNewTaskTestCase(TestCase):
    def setUp(self):
        _setUp(self)


class PostTaskOverviewTestCase(TestCase):
    def setUp(self):
        _setUp(self)


class PostGroupsTestCase(TestCase):
    def setUp(self):
        _setUp(self)


class PostManageGroupTestCase(TestCase):
    def setUp(self):
        _setUp(self)
