from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from accounts.models import User
from categories.models import Category
from jobsapp.api.serializers import JobSerializer, NewJobSerializer
from jobsapp.models import Company, Job
from tags.models import Tag


class TestJobSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            role="employer",
        )
        self.company = Company.objects.create(user=self.user, name="Test Company")
        self.category = Category.objects.create(
            name="Software Engineering",
            description="Software roles",
        )
        self.job = Job.objects.create(
            title="Test Job",
            description="Test Description",
            location="Test Location",
            salary=100000,
            type="1",
            application_deadline=timezone.now() + timedelta(days=30),
            user=self.user,
            company=self.company,
            category=self.category,
        )

    def test_job_serializer(self):
        serializer = JobSerializer(self.job)
        self.assertEqual(serializer.data["title"], "Test Job")
        self.assertEqual(serializer.data["description"], "Test Description")
        self.assertEqual(serializer.data["location"], "Test Location")
        self.assertEqual(serializer.data["salary"], 100000)
        self.assertEqual(serializer.data["company"]["id"], self.company.id)
        self.assertEqual(serializer.data["category"]["id"], self.category.id)
        self.assertEqual(serializer.data["category"]["name"], "Software Engineering")


class TestNewJobSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="employer1@example.com",
            password="testpassword",
            role="employer",
        )
        self.company = Company.objects.create(user=self.user, name="Test Company")
        self.category = Category.objects.create(
            name="Web Development",
            description="Web development roles",
        )
        self.tag = Tag.objects.create(name="Python")
        self.job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "location": "Test Location",
            "salary": 100000,
            "type": "1",
            "application_deadline": (timezone.now() + timedelta(days=30)).isoformat(),
            "category": self.category.id,
            "company": self.company.id,
            "website": "https://www.testcompany.com",
            "tags": [self.tag.id],
        }
        self.request_factory = APIRequestFactory()

    def _request(self):
        request = self.request_factory.post("/")
        request.user = self.user
        return request

    def test_new_job_serializer(self):
        serializer = NewJobSerializer(data=self.job_data, context={"request": self._request()})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        job = serializer.save(user=self.user)
        self.assertEqual(job.title, self.job_data["title"])
        self.assertEqual(job.description, self.job_data["description"])
        self.assertEqual(job.location, self.job_data["location"])
        self.assertEqual(job.salary, self.job_data["salary"])
        self.assertEqual(job.type, self.job_data["type"])
        self.assertEqual(job.category_id, self.category.id)
        self.assertEqual(job.company_id, self.company.id)
        self.assertEqual(job.website, self.job_data["website"])
        self.assertEqual(list(job.tags.values_list("id", flat=True)), self.job_data["tags"])
        self.assertEqual(job.user, self.user)

    def test_new_job_rejects_other_users_company(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpassword",
            role="employer",
        )
        other_company = Company.objects.create(user=other_user, name="Other Co")
        data = {**self.job_data, "company": other_company.id}
        serializer = NewJobSerializer(data=data, context={"request": self._request()})
        self.assertFalse(serializer.is_valid())
        self.assertIn("company", serializer.errors)
