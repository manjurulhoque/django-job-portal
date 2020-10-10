from django.test import TestCase
import pytest
from tests.factories import UserFactory
from jobsapp import models


# Create your tests here.
@pytest.mark.django_db
class TestExampe:
    def test__exemple__ok(self):
        user = UserFactory(first_name='Geeks', last_name='.CAT')
        assert user.first_name == 'Geeks'
