import factory
from jobsapp.models import User, Job
import pytest


# List of factories
class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    admin = False


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job
        django_get_or_create = ('type')

    user = factory.SubFactory('jobsapp.tests.UserFactory')
    title = factory.Sequence(lambda n: 'Title %d' % n)
    description = factory.Sequence(lambda n: 'Description %d' % n)
    type = '1'


# Create your tests here.
@pytest.mark.django_db
class TestExampe:
    def test__exemple__ok(self):
        x = "my simple app test"
        assert 'simple app' in x
