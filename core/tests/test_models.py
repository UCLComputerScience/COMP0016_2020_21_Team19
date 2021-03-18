import datetime

from django.test import TestCase
from core.models import *

class TaskTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="")
        self.task = Task.objects.create(title="", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
    
    def test_mark_as_complete(self):
        """
        The `completed` attribute of a Task should be
        set to True through the `mark_as_complete()` method.
        """
        self.task.completed = False
        self.task.mark_as_complete()
        self.assertTrue(self.task.completed)
    
    def test_mark_as_incomplete(self):
        """
        The `completed` attribute of a Task should be
        set to False through the `mark_as_complete()` method.
        """
        self.task.completed = True
        self.task.mark_as_incomplete()
        self.assertFalse(self.task.completed)
    
class QuestionTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="")
        self.task = Task.objects.create(title="", group=self.group, due_date=datetime.datetime(2021, 7, 3), due_time=datetime.time(10, 0))
        self.likert_question = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.LIKERT_ASC)
        self.traffic_light_question = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.TRAFFIC_LIGHT)
        self.numerical_question = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.NUMERICAL_ASC)
        self.text_question = Question.objects.create(task=self.task, description="", response_type=Question.ResponseType.TEXT_NEUTRAL)

    def test_is_text_neutral(self):
        """
        The `is_text_neutral` property should return False if the
        `response_type` of a Question is not `Question.ResponseType.TEXT_NEUTRAL`.
        """
        self.assertFalse(self.likert_question.is_text_neutral)
    
    def test_is_text_positive(self):
        """
        The `is_text_positive` property should return False if the
        `response_type` of a Question is not `Question.ResponseType.TEXT_POSITIVE`.
        """
        self.assertFalse(self.likert_question.is_text_positive)
    
    def test_is_text_negative(self):
        """
        The `is_text_negative` property should return False if the
        `response_type` of a Question is not `Question.ResponseType.TEXT_NEGATIVE`.
        """
        self.assertFalse(self.likert_question.is_text_negative)

    def test_get_labels_likert(self):
        """
        The `get_labels()` method property should return the list
        ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'] if the
        `response_type` of a Question is `Question.ResponseType.LIKERT_ASC`
        or `Question.ResponseType.LIKERT_DESC`.
        """
        expected = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
        self.assertEqual(self.likert_question.get_labels(), expected)
    
    def test_get_labels_traffic_light(self):
        """
        The `get_labels()` method property should return the list
        ['Red', 'Yellow', 'Green'] if the `response_type`
        of a Question is `Question.ResponseType.TRAFFIC_LIGHT`.
        """
        expected = ['Red', 'Yellow', 'Green']
        self.assertEqual(self.traffic_light_question.get_labels(), expected)
    
    def test_get_labels_numerical(self):
        """
        The `get_labels()` method property should return the list
        ['1', '2', '3', '4', '5'] if the `response_type`
        of a Question is `Question.ResponseType.NUMERICAL_ASC`
        or `Question.ResponseType.NUMERICAL_DESC`.
        """
        expected = ['1', '2', '3', '4', '5']
        self.assertEqual(self.numerical_question.get_labels(), expected)

    def test_get_values_list_likert(self):
        """
        The `get_values_list()` method property should return the list
        [1, 2, 3, 4, 5] if the `response_type` of a Question is
        `Question.ResponseType.LIKERT_ASC` or `Question.ResponseType.LIKERT_DESC`.
        """
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(self.likert_question.get_values_list(), expected)

    def test_get_values_list_traffic_light(self):
        """
        The `get_values_list()` method property should return the list
        [
            self.traffic_light_question.traffic_light_sad_value,
            self.traffic_light_question.traffic_light_neutral_value,
            self.traffic_light_question.traffic_light_happy_value
        ]
        if the `response_type` of a Question is `Question.ResponseType.TRAFFIC_LIGHT`.
        """
        expected = [
            self.traffic_light_question.traffic_light_sad_value,
            self.traffic_light_question.traffic_light_neutral_value,
            self.traffic_light_question.traffic_light_happy_value
        ]
        self.assertEqual(self.traffic_light_question.get_values_list(), expected)

    def test_get_values_list_numerical(self):
        """
        The `get_values_list()` method property should return the list
        ['1', '2', '3', '4', '5'] if the `response_type`
        of a Question is `Question.ResponseType.NUMERICAL_ASC`
        or `Question.ResponseType.NUMERICAL_DESC`.
        """
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(self.numerical_question.get_values_list(), expected)

    def test_get_values_list_text(self):
        """
        The `get_values_list()` method property should return None if the `response_type`
        of a Question is not `Question.ResponseType.NUMERICAL_ASC`,
        `Question.ResponseType.NUMERICAL_DESC`,
        `Question.ResponseType.NUMERICAL_ASC`
        or `Question.ResponseType.NUMERICAL_DESC`.
        """
        expected = None
        self.assertEqual(self.text_question.get_values_list(), expected)