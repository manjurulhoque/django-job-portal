from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from tests.factories.category_factory import CategoryFactory
from tests.factories.job_factory import JobFactory
from tests.factories.tag_factory import TagFactory
from tests.factories.user_factory import UserFactory

User = get_user_model()


class TestCommonApiViews(APITestCase):
    def setUp(self):
        # Create test data
        self.categories = CategoryFactory.create_batch(10)
        self.jobs = JobFactory.create_batch(5)
        self.user = UserFactory(role="employee")

    def test_categories_list_api_view(self):
        """Test the categories list API endpoint"""
        url = reverse("categories:categories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()), 15
        )  # job factory creates 5 more categories

    def test_jobs_list_api_view(self):
        """Test the jobs list API endpoint"""
        url = reverse("jobs-api:job-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

    def test_job_detail_api_view(self):
        """Test the job detail API endpoint"""
        job = self.jobs[0]
        url = reverse("jobs-api:job-detail", kwargs={"pk": job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], job.title)

    def test_search_api_view(self):
        """Test the search API endpoint"""
        url = reverse("jobs-api:search")
        response = self.client.get(
            url, {"location": "Dhaka", "position": "Software Engineer"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_apply_job_api_view(self):
        """Test the apply job API endpoint"""
        # apply job without authentication
        url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # apply job with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["job"], self.jobs[0].id)

        # test already apply to same job
        url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applied_jobs_api_view(self):
        """Test the applied jobs API endpoint"""
        # get applied jobs without authentication
        applied_jobs_url = reverse("jobs-api:applied-jobs")
        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # get applied jobs with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        # apply job
        url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get applied jobs again
        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["applicant"]["job"]["id"], self.jobs[0].id)

    def test_already_applied_api_view(self):
        """Test the already applied API endpoint"""
        # check without authentication
        url = reverse("jobs-api:applied-for-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication before applying
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_applied"])

        # apply for the job
        apply_url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        self.client.post(apply_url, {"job": self.jobs[0].id})

        # check after applying
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["is_applied"])


class TestEmployerApiViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods"""
        cls.employer = UserFactory(role="employer")
        cls.employee = UserFactory(role="employee")
        cls.tag = TagFactory()
        cls.job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "location": "Test Location",
            "salary": 10000,
            "type": "1",  # Full time
            "category": "web-development",
            "last_date": "2024-12-31",
            "company_name": "Test Company",
            "company_description": "A great company to work for",
            "website": "www.testcompany.com",
            "tags": [cls.tag.pk],
        }

    def setUp(self):
        """Set up test client for each test method"""
        self.job = JobFactory(user=self.employer)
        self.client = self.client_class()

    def test_dashboard_api_view(self):
        """Test the dashboard API endpoint"""
        # check without authentication
        url = reverse("jobs-api:employer-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.job.id)

    def test_job_create_api_view(self):
        """Test the job create API endpoint"""
        url = reverse("jobs-api:employer-job-create")
        response = self.client.post(url, self.job_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(url, self.job_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Test Job")

    def test_applicants_list_api_view(self):
        """Test the applicants list API endpoint"""
        url = reverse("jobs-api:employer-applicants-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_applicants_per_job_list_api_view(self):
        """Test the applicants per job list API endpoint"""
        url = reverse(
            "jobs-api:employer-applicants-per-job-list", kwargs={"job_id": self.job.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_update_applicant_status_api_view(self):
        """Test the update applicant status API endpoint"""
        # apply for the job
        self.client.force_authenticate(user=self.employee)
        apply_url = reverse("jobs-api:apply-job", kwargs={"job_id": self.job.id})
        self.client.post(apply_url, {"job": self.job.id})

        # update applicant status without authentication
        self.client.logout()
        url = reverse(
            "jobs-api:employer-update-applicant-status",
            kwargs={"applicant_id": self.employee.id, "status_code": 1},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check with authentication
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse(
            "jobs-api:employer-update-applicant-status",
            kwargs={"applicant_id": self.job.id, "status_code": 10},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
