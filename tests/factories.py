import factory

from accounts.models import User
from jobsapp.models import Job


# List of factories
class UserFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = User
        django_get_or_create = ("first_name", "last_name")

    first_name = "John"
    last_name = "Doe"


class JobFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = Job
        django_get_or_create = "type"

    user = factory.SubFactory("jobsapp.tests.UserFactory")
    title = factory.Sequence(lambda n: "Title %d" % n)
    description = factory.Sequence(lambda n: "Description %d" % n)
    type = "1"
