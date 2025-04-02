import factory
from django.utils import timezone
from datetime import timedelta
import random

from jobsapp.models import Job, JOB_TYPE
from tests.factories.category_factory import CategoryFactory
from tests.factories.user_factory import UserFactory


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Sequence(lambda n: f"Job {n}")
    description = factory.Faker("sentence")
    location = factory.Faker("city")
    salary = factory.Faker("random_int", min=1000, max=100000)
    type = factory.Faker("random_element", elements=JOB_TYPE)
    # last_date = factory.Faker("date_between", start_date="-30d", end_date="now")
    last_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=random.randint(1, 30)))
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)
