from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from jobsapp.models import Applicant, Company
from tests.factories.category_factory import CategoryFactory
from tests.factories.job_factory import CompanyFactory, JobFactory
from tests.factories.tag_factory import TagFactory
from tests.factories.user_factory import UserFactory

User = get_user_model()


class TestCommonApiViews(APITestCase):
    def setUp(self):
        self.categories = CategoryFactory.create_batch(10)
        self.jobs = JobFactory.create_batch(5)
        self.user = UserFactory(role="employee")

    def test_categories_list_api_view(self):
        url = reverse("categories:categories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 15)

    def test_jobs_list_api_view(self):
        url = reverse("jobs-api:job-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 5)
        self.assertEqual(len(response.json()["results"]), 5)

    def test_jobs_list_filter_by_category(self):
        category = self.jobs[0].category
        url = reverse("jobs-api:job-list")
        response = self.client.get(url, {"category": category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.json()["count"], 1)
        for job in response.json()["results"]:
            self.assertEqual(job["category"]["id"], category.id)

    def test_job_detail_api_view(self):
        job = self.jobs[0]
        url = reverse("jobs-api:job-detail", kwargs={"pk": job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], job.title)
        self.assertEqual(response.json()["category"]["id"], job.category_id)

    def test_search_api_view(self):
        url = reverse("jobs-api:search")
        response = self.client.get(
            url, {"location": "Dhaka", "position": "Software Engineer"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_api_view_filter_by_category(self):
        category = self.jobs[0].category
        url = reverse("jobs-api:search")
        response = self.client.get(url, {"category": category.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for job in response.json():
            self.assertEqual(job["category"]["id"], category.id)

    def test_apply_job_api_view(self):
        url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["job"], self.jobs[0].id)

        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applied_jobs_api_view(self):
        applied_jobs_url = reverse("jobs-api:applied-jobs")
        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.post(url, {"job": self.jobs[0].id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(applied_jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["applicant"]["job"]["id"], self.jobs[0].id)

    def test_already_applied_api_view(self):
        url = reverse("jobs-api:applied-for-job", kwargs={"job_id": self.jobs[0].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_applied"])

        apply_url = reverse("jobs-api:apply-job", kwargs={"job_id": self.jobs[0].id})
        self.client.post(apply_url, {"job": self.jobs[0].id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["is_applied"])


class TestEmployerApiViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employer = UserFactory(role="employer")
        cls.employee = UserFactory(role="employee")
        cls.company = CompanyFactory(user=cls.employer)
        cls.category = CategoryFactory()
        cls.tag = TagFactory()
        cls.job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "location": "Test Location",
            "salary": 10000,
            "type": "1",
            "category": cls.category.id,
            "company": cls.company.id,
            "application_deadline": (timezone.now() + timedelta(days=30)).isoformat(),
            "website": "https://www.testcompany.com",
            "tags": [cls.tag.pk],
        }

    def setUp(self):
        self.job = JobFactory(user=self.employer, company=self.company)
        self.client = self.client_class()

    def test_dashboard_api_view(self):
        url = reverse("jobs-api:employer-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.job.id)

    def test_job_create_api_view(self):
        url = reverse("jobs-api:employer-job-create")
        response = self.client.post(url, self.job_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.post(url, self.job_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Test Job")
        self.assertEqual(response.json()["category"]["id"], self.category.id)
        self.assertEqual(response.json()["company"]["id"], self.company.id)

    def test_job_create_rejects_other_company(self):
        other_company = CompanyFactory()
        url = reverse("jobs-api:employer-job-create")
        self.client.force_authenticate(user=self.employer)
        response = self.client.post(url, {**self.job_data, "company": other_company.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_companies_list_api_view(self):
        url = reverse("jobs-api:employer-companies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.company.id)

    def test_applicants_list_api_view(self):
        url = reverse("jobs-api:employer-applicants-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_applicants_per_job_list_api_view(self):
        url = reverse(
            "jobs-api:employer-applicants-per-job-list", kwargs={"job_id": self.job.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_update_applicant_status_api_view(self):
        self.client.force_authenticate(user=self.employee)
        apply_url = reverse("jobs-api:apply-job", kwargs={"job_id": self.job.id})
        self.client.post(apply_url, {"job": self.job.id})
        applicant = Applicant.objects.get(user=self.employee, job=self.job)

        self.client.logout()
        url = reverse(
            "jobs-api:employer-update-applicant-status",
            kwargs={"applicant_id": applicant.id, "status_code": 1},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.employer)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse(
                "jobs-api:employer-update-applicant-status",
                kwargs={"applicant_id": 999999, "status_code": 1},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
