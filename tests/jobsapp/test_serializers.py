from django.test import TestCase
from jobsapp.api.serializers import JobSerializer
from django.utils import timezone
from datetime import timedelta
from jobsapp.models import Job
from accounts.models import User


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
