from django.test import TestCase

from core.models import *
from respondent.models import *
from surveyor.models import *


class RespondentTestCase(TestCase):
    def setUp(self):
        Respondent.objects.create(firstname="John", surname="Doe")

    def test_get_str(self):
        respondent = Respondent.objects.get(firstname="John")
        str(respondent)
