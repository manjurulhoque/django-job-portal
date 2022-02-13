from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import translation

from accounts.models import User
from jobsapp.models import Applicant, Job


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.language_code = translation.get_language()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.valid_job = {
            "title": "Junior Software Engineer",
            "description": "Looking for Python developer",
            "salary": 35000,
            "location": "Dhaka, Bangladesh",
            "type": "1",
            "category": "web-development",
            "last_date": datetime.now() + timedelta(days=30),
            "company_name": "Dev Soft",
            "company_description": "A foreign country",
            "website": "www.devsoft.com",
        }
        cls.employer = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "employer@gmail.com",
            "role": "employer",
            "password": "123456",
        }
        cls.user = User.objects.create(**cls.employer)
        cls.job = Job(**cls.valid_job)
        cls.job.user = cls.user
        cls.job.save()


class TestJobModel(BaseTest):
    def test_get_absolute_url(self):
        self.assertURLEqual(self.job.get_absolute_url(), f"/{self.language_code}/jobs/1/")

    def test_title_max_length(self):
        max_length = self.job._meta.get_field("title").max_length
        self.assertEqual(max_length, 300)

    def test_title_label(self):
        field_label = self.job._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")


class TestApplicantModel(BaseTest):
    @classmethod
    def setUpTestData(cls) -> None:
        super(TestApplicantModel, cls).setUpTestData()
        cls.applicant = Applicant.objects.create(user=cls.user, job=cls.job)

    def test_str(self):
        self.assertEqual(self.applicant.__str__(), self.user.get_full_name())
