import factory
from django.utils import timezone
from datetime import timedelta
import random

from jobsapp.models import Company, Job, JobType
from tests.factories.category_factory import CategoryFactory
from tests.factories.user_factory import UserFactory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Company {n}")
    description = factory.Faker("sentence")


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Sequence(lambda n: f"Job {n}")
    description = factory.Faker("sentence")
    location = factory.Faker("city")
    salary = factory.Faker("random_int", min=1000, max=100000)
    type = factory.Faker("random_element", elements=[choice[0] for choice in JobType.choices])
    application_deadline = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=random.randint(1, 30))
    )
    category = factory.SubFactory(CategoryFactory)
    company = factory.SubFactory(CompanyFactory)
    user = factory.SelfAttribute("company.user")
