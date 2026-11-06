from datetime import timedelta

from django.test import TestCase
from django.utils import timezone, translation

from accounts.models import User
from categories.models import Category
from jobsapp.models import Applicant, Company, Job


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.language_code = translation.get_language()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            email="employer@gmail.com",
            password="123456",
            role="employer",
            first_name="John",
            last_name="Doe",
        )
        cls.company = Company.objects.create(user=cls.user, name="Dev Soft")
        cls.category = Category.objects.create(
            name="Web Development",
            description="Web development roles",
        )
        cls.job = Job.objects.create(
            title="Junior Software Engineer",
            description="Looking for Python developer",
            salary=35000,
            location="Dhaka, Bangladesh",
            type="1",
            application_deadline=timezone.now() + timedelta(days=30),
            website="https://www.devsoft.com",
            user=cls.user,
            company=cls.company,
            category=cls.category,
        )


class TestJobModel(BaseTest):
    def test_get_absolute_url(self):
        self.assertURLEqual(self.job.get_absolute_url(), f"/{self.language_code}/jobs/{self.job.id}/")

    def test_title_max_length(self):
        max_length = self.job._meta.get_field("title").max_length
        self.assertEqual(max_length, 300)

    def test_title_label(self):
        field_label = self.job._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_category_relation(self):
        self.assertEqual(self.job.category.name, "Web Development")
        self.assertEqual(self.job.company.name, "Dev Soft")


class TestApplicantModel(BaseTest):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.applicant = Applicant.objects.create(user=cls.user, job=cls.job)

    def test_str(self):
        self.assertEqual(self.applicant.__str__(), self.user.get_full_name())
