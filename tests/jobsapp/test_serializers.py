from django.test import TestCase
from jobsapp.api.serializers import JobSerializer, NewJobSerializer
from django.utils import timezone
from datetime import timedelta
from jobsapp.models import Job
from accounts.models import User
from tags.models import Tag
from django.forms.models import model_to_dict


class TestJobSerializer(TestCase):
    """
    Unit tests for the JobSerializer
    """

    def setUp(self):
        self.job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "location": "Test Location",
            "salary": 100000,
            "created_at": timezone.now(),
            "last_date": timezone.now() + timedelta(days=30),
            "user": User.objects.create_user(
                email="testuser@example.com",
                password="testpassword",
            ),
        }

    def test_job_serializer(self):
        """
        Test the JobSerializer
        """
        job = Job.objects.create(**self.job_data)
        serializer = JobSerializer(job)
        self.assertEqual(serializer.data["title"], "Test Job")
        self.assertEqual(serializer.data["description"], "Test Description")
        self.assertEqual(serializer.data["location"], "Test Location")
        self.assertEqual(serializer.data["salary"], 100000)
        # Format the datetime to match DRF's UTC format
        expected_datetime = self.job_data["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(serializer.data["created_at"], expected_datetime)


class TestNewJobSerializer(TestCase):
    """
    Unit tests for the NewJobSerializer
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="employer1@example.com",
            password="testpassword",
            role="employer",
        )
        self.tag = Tag.objects.create(name="Python")
        self.job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "location": "Test Location",
            "salary": 100000,
            "created_at": timezone.now(),
            "last_date": timezone.now() + timedelta(days=30),
            "type": "1",  # Full time
            "category": "web-development",
            "company_name": "Test Company",
            "company_description": "A great company to work for",
            "website": "www.testcompany.com",
            "tags": [self.tag.id],
            "user": self.user.id,
        }

    def tearDown(self):
        self.user.delete()
        self.tag.delete()

    def test_new_job_serializer(self):
        # Create serializer with context
        # serializer = NewJobSerializer(data=self.job_data, context={'request': type('Request', (), {'user': self.user})()})
        serializer = NewJobSerializer(data=self.job_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        job = serializer.save()
        self.assertEqual(job.title, self.job_data["title"])
        self.assertEqual(job.description, self.job_data["description"])
        self.assertEqual(job.location, self.job_data["location"])
        self.assertEqual(job.salary, self.job_data["salary"])
        self.assertEqual(job.type, self.job_data["type"])
        self.assertEqual(job.category, self.job_data["category"])
        self.assertEqual(job.company_name, self.job_data["company_name"])
        self.assertEqual(job.company_description, self.job_data["company_description"])
        self.assertEqual(job.website, self.job_data["website"])
        self.assertEqual(list(job.tags.values_list("id", flat=True)), self.job_data["tags"])
        self.assertEqual(job.user, self.user)

    def test_new_job_with_logged_in_user(self):
        self.client.force_login(self.user)
        serializer = NewJobSerializer(
            data=self.job_data,
            context={"request": type("Request", (), {"user": self.user})()},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        job = serializer.save()
        self.assertEqual(job.user, self.user)
