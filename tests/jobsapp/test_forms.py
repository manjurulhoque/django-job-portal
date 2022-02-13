from datetime import datetime, timedelta
from http import HTTPStatus
from django.test import TestCase

from accounts.models import User
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job
from tags.models import Tag


class TestCreateJobForm(TestCase):
    def setUp(self) -> None:
        self.valid_job = {
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
            "tags": [Tag.objects.create(name="Development").id],
        }
        self.employer = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "employer@gmail.com",
            "role": "employer",
            "password": "123456",
        }
        self.user = User.objects.create(**self.employer)

    def test_valid_and_save_form(self):
        form = CreateJobForm(data=self.valid_job)
        valid = form.is_valid()
        self.assertTrue(valid)

        job = form.save(commit=False)
        job.user = self.user
        job.save()

        self.assertIsInstance(job, Job, "Not a job")

    def test_field_required(self):
        form = CreateJobForm(data={})
        form.is_valid()

        self.assertEqual(form.errors["title"], ["This field is required."])
