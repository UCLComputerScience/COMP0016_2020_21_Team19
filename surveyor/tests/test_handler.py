import datetime
import io
import pandas as pd
import uuid

from django.http import HttpRequest, Http404
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.forms import formset_factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from surveyor import handler
from surveyor.forms import *
from surveyor.models import *
from respondent.models import *
from core.models import *

def _setUp(testcase):
    testcase.factory = RequestFactory()

    testcase.surveyor_user = User.objects.create_user(username='surveyor', email='email@email.com', password='activityleague')
    testcase.surveyor = Surveyor.objects.create(firstname="Firstname", surname="Surname", user=testcase.surveyor_user)
    
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

    def setUp(self):
        _setUp(self)
        

    def test_returns_correct_dict(self):
        request = self.factory.get(reverse('new-task'))
        request.user = self.surveyor_user
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
        request.user = self.surveyor_user
        group_ids = GroupSurveyor.objects.filter(surveyor=self.surveyor).values_list('group', flat=True)
        groups = Group.objects.filter(id__in=group_ids)
        response = handler.get_new_task(groups, request, self.surveyor)
        formset = response['formset']
        questions = [self.question_1, self.question_2, self.question_3]
        self.assertEqual(len(questions), len(formset))


    def test_returns_correct_templates(self):
        """
        Check we get the TaskTemplates that have been created by the Surveyor.
        """
        request = self.factory.get(reverse('new-task'))
        request.user = self.surveyor_user
        group_ids = GroupSurveyor.objects.filter(surveyor=self.surveyor).values_list('group', flat=True)
        groups = Group.objects.filter(id__in=group_ids)
        templates = handler.get_new_task(groups, request, self.surveyor)['templates']
        self.assertTrue(self.task_template in templates and len(templates) == 1)
        

    def test_taskform_fields_correct(self):
        """
        We should have a TaskForm with fields ('title', 'due_date', 'due_time', 'group').
        """
        request = self.factory.get(reverse('new-task'))
        request.user = self.surveyor_user
        taskform = handler.get_new_task(None, request, None)['taskform']
        self.assertEqual(taskform.fields.keys(), {'title', 'due_date', 'due_time', 'group'})    


class PostOrganisationTestCase(TestCase):

    def setUp(self):
        _setUp(self)
    
    def test_delete_surveyor(self):
        """
        Passing request_type 'delete_surveyor' should delete the corresponding Surveyor object.
        """
        payload = {'request_type': 'delete_surveyor', 'surveyor': self.surveyor.id}
        request = self.factory.post(reverse('organisation'), payload)
        handler.post_organisation(request, self.surveyor)
        self.assertFalse(Surveyor.objects.filter(firstname="Firstname").exists())

    def test_invite_surveyor(self):
        """
        Passing request_type 'invite' and email should create a UserInvitation object.
        """
        payload = {'request_type': 'invite', 'email': 'mail@mail.com'}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.surveyor_user
        handler.post_organisation(request, self.surveyor)
        self.assertTrue(UserInvitation.objects.filter(email='mail@mail.com').exists())

    def test_invite_multiple_surveyors(self):
        """
        Uploading a file of user emails should create UserInvitation objects with the same email
        as those in the file and no more.
        """
        df = pd.DataFrame([[f'surveyor{i}@mail.com'] for i in range(3)])
        output_stream = io.BytesIO()
        df.to_excel(output_stream, index=False)
        file = SimpleUploadedFile('surveyors.xlsx', output_stream.getvalue())
        payload = {'request_type': 'import', 'file': file}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.surveyor_user
        handler.post_organisation(request, self.surveyor)
        for i in range(3):
            self.assertTrue(UserInvitation.objects.filter(email=f'surveyor{i}@mail.com').exists())
    
    def test_invite_multiple_surveyors_invalid(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'import' and a valid 'file'
        should create UserInvitation objects corresponding to the emails in the imported file.
        If there are invalid emails in the file, we should raise Htp404.
        """
        df = pd.DataFrame([['surveyormail.com']])
        output_stream = io.BytesIO()
        df.to_excel(output_stream, index=False)
        file = SimpleUploadedFile('surveyors.xlsx', output_stream.getvalue())
        payload = {'request_type': 'import', 'file': file}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.surveyor_user
        with self.assertRaises(Http404, msg="Something was wrong with your file!"):
            handler.post_organisation(request, self.surveyor)


class PostNewTaskTestCase(TestCase):
    def setUp(self):
        _setUp(self)
    
    def test_delete_template(self):
        """
        If `request` has a parameter 'delete', we should delete the `TaskTemplate`
        associated with the id passed as the argument.
        """
        id = self.task_template.id
        payload = {'delete': id, 'template': id}
        request = self.factory.post(reverse('new-task'), payload)
        request.user = self.surveyor_user
        handler.post_new_task(request, self.surveyor)
        self.assertFalse(TaskTemplate.objects.filter(id=id).exists())
        
    def test_delete_template_invalid(self):
        """
        If we try to delete a template that does not exist with a valid UUID string,
        there should not be an exception.
        """
        id = uuid.uuid4()
        payload = {'delete': id, 'template': id}
        request = self.factory.post(reverse('new-task'), payload)
        request.user = self.surveyor_user
        with self.assertRaises(TaskTemplate.DoesNotExist):
            handler.post_new_task(request, self.surveyor)
    
    def test_save_template(self):
        """
        If we post a valid form and formset, we should see a new TaskTemplate created.
        """
        payload = {
            'save': 'save',
            'title': 'Title',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-link': "url.com",
            'form-0-description': "Random Task",
            'form-0-response_type': "1",
        }
        request = self.factory.post(reverse('new-task'), payload)
        request.user = self.surveyor_user
        handler.post_new_task(request, self.surveyor)
        self.assertTrue(TaskTemplate.objects.filter(name='Title').exists())
    
    def test_save_template_invalid(self):
        """
        Posting an invalid form (missing a few fields) should raise a Http404 error.
        """
        payload = {
            'save': 'save',
            'title': 'Title',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-link': "url.com",
            'form-0-response_type': "1",
        }
        request = self.factory.post(reverse('new-task'), payload)
        request.user = self.surveyor_user
        with self.assertRaises(Http404):
            handler.post_new_task(request, self.surveyor)
    
    def test_submit_task(self):
        """
        Submitting a valid task should create a new corresponding Task object.
        """
        payload = {
            'submit': 'submit',
            'title': 'Title',
            'group': self.group_1.id,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-MIN_NUM_FORMS': '',
            'form-0-link': "url.com",
            'form-0-description': "Random Task",
            'form-0-response_type': "1",
            'due_date': '2021-04-21',
            'due_time': '20:00',
        }
        request = self.factory.post(reverse('new-task'), payload)
        request.user = self.surveyor_user
        handler.post_new_task(request, self.surveyor)
        self.assertTrue(Task.objects.filter(title='Title').exists())


class PostTaskOverviewTestCase(TestCase):
    def setUp(self):
        _setUp(self)
    
    def test_mark_task_as_complete(self):
        """
        Passing request 'complete' and task should change the completed property
        of the associated Task object to True.
        """
        self.task.completed = False
        payload = {'request': 'complete', 'task': self.task.id}
        request = self.factory.post(reverse('task_overview', args=[self.task.id]), payload)
        request.user = self.surveyor_user
        handler.post_task_overview(request)
        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.completed)

    def test_mark_task_as_incomplete(self):
        """
        Passing request 'incomplete' and task should change the completed property
        of the associated Task object to False.
        """
        self.task.completed = True
        payload = {'request': 'incomplete', 'task': self.task.id}
        request = self.factory.post(reverse('task_overview', args=[self.task.id]), payload)
        request.user = self.surveyor_user
        handler.post_task_overview(request)
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.completed)

    def test_delete_task(self):
        """
        Passing request 'delete' and a task ID into a POST request should
        result in the corresponding Task object being deleted.
        """
        payload = {'request': 'delete', 'task': self.task.id}
        request = self.factory.post(reverse('task_overview', args=[self.task.id]), payload)
        request.user = self.surveyor_user
        handler.post_task_overview(request)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class PostGroupsTestCase(TestCase):
    def setUp(self):
        _setUp(self)
    
    def test_new_group(self):
        """
        A POST request to `/groups` where 'request_type' = 'new_group' should
        create a Group instance.
        """
        payload = {'request_type': 'new_group', 'name': 'Test Group'}
        request = self.factory.post(reverse('groups'), payload)
        request.user = self.surveyor_user
        handler.post_groups(request)
        self.assertTrue(Group.objects.filter(name='Test Group').exists())

    def test_new_group_invalid(self):
        """
        A POST request to `/groups` with an invalid payload (missing name value)
        should raise a Http404 error.
        """
        payload = {'request_type': 'new_group', 'name': ''}
        request = self.factory.post(reverse('groups'), payload)
        request.user = self.surveyor_user
        with self.assertRaises(Http404, msg='Something went wrong!'):
            handler.post_groups(request)

    def test_delete_group(self):
        """
        A POST request to `/groups` where 'request_type' = 'new_group' should
        create a Group instance.
        """
        payload = {'request_type': 'delete_group', 'group': self.group_1.id}
        request = self.factory.post(reverse('groups'), payload)
        request.user = self.surveyor_user
        handler.post_groups(request)
        self.assertFalse(Group.objects.filter(id=self.group_1.id).exists())


class PostManageGroupTestCase(TestCase):
    def setUp(self):
        _setUp(self)
        self.respondent_user = User.objects.create_user('respondent@email.com', 'activityleague')
        self.respondent = Respondent.objects.create(firstname="Firstname", surname="Surname", user=self.respondent_user)

    def test_delete_respondent(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'delete_participant' and a valid 'respondent'
        id should delete the associated GroupRespondent object. 
        """
        self.group_respondent_1 = GroupRespondent.objects.create(group=self.group_1, respondent=self.respondent)
        payload = {'request_type': 'delete_participant', 'respondent': self.respondent.id}
        request = self.factory.post(reverse('manage-group', args=[self.group_1.id]), payload)
        handler.post_manage_group(request, self.group_1.id)
        self.assertFalse(GroupRespondent.objects.filter(respondent=self.respondent).exists())

    def test_invite_respondent(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'invite' and a valid 'email'
        should create a corresponding UserInvitation object. 
        """
        payload = {'request_type': 'invite', 'email': 'respondent@mail.com'}
        request = self.factory.post(reverse('manage-group', args=[self.group_1.id]), payload)
        request.user = self.surveyor_user
        handler.post_manage_group(request, self.group_1.id)
        self.assertTrue(UserInvitation.objects.filter(email='respondent@mail.com').exists())

    def test_invite_respondent_with_surveyor_email(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'invite' and the email
        of a Surveyor should raise a Http404 exception. 
        """
        payload = {'request_type': 'invite', 'email': self.surveyor_user.email}
        request = self.factory.post(reverse('manage-group', args=[self.group_1.id]), payload)
        request.user = self.surveyor_user
        with self.assertRaises(Http404, msg="You cannot invite a Surveyor to a Group!"):
            handler.post_manage_group(request, self.group_1.id)

    def test_invite_multiple_respondents(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'import' and a valid 'file'
        should create UserInvitation objects corresponding to the emails in the imported
        file. 
        """
        df = pd.DataFrame([[f'respondent{i}@mail.com'] for i in range(3)])
        output_stream = io.BytesIO()
        df.to_excel(output_stream, index=False)
        file = SimpleUploadedFile('respondents.xlsx', output_stream.getvalue())
        payload = {'request_type': 'import', 'file': file}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.surveyor_user
        handler.post_manage_group(request, self.group_1.id)
        for i in range(3):
            self.assertTrue(UserInvitation.objects.filter(email=f'respondent{i}@mail.com').exists())

    def test_invite_multiple_respondents_invalid(self):
        """
        A POST request to `/manage-group` with 'request_type' = 'import' and a valid 'file'
        should create UserInvitation objects corresponding to the emails in the imported file.
        If there are invalid emails in the file, we should raise a Http404 error.
        """
        df = pd.DataFrame([['respondentmail.com']])
        output_stream = io.BytesIO()
        df.to_excel(output_stream, index=False)
        file = SimpleUploadedFile('respondents.xlsx', output_stream.getvalue())
        payload = {'request_type': 'import', 'file': file}
        request = self.factory.post(reverse('organisation'), payload)
        request.user = self.surveyor_user
        with self.assertRaises(Http404, msg="Something was wrong with your file!"):
            handler.post_manage_group(request, self.group_1.id)