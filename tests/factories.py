import datetime

import factory
import factory.fuzzy
from accounts.models import User
from jobsapp.models import Job

JOB_CHOICE = [Job.JOB_TYPE_FULL_TIME, Job.JOB_TYPE_PART_TIME, Job.JOB_TYPE_INTERNSHIP]


# List of factories
class UserFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = User
        django_get_or_create = ("first_name", "last_name")

    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = "Doe"


class JobFactory(factory.django.DjangoModelFactory):  # type: ignore

    class Meta:
        model = Job
        django_get_or_create = ("type", "category", 'company_name', 'title')

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Title %d" % n)
    description = factory.Sequence(lambda n: "Description %d" % n)
    company_description = factory.LazyAttribute(lambda n: f"Company Description {n.company_name}")
    company_name = factory.Faker('company')
    category = factory.fuzzy.FuzzyChoice(['Marketing', 'backend', 'frontend', 'Data Science'])
    type = factory.fuzzy.FuzzyChoice(JOB_CHOICE)
    last_date = datetime.datetime.now()
