from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from categories.models import Category
from jobsapp.forms import CreateJobForm
from jobsapp.models import Company, Job
from tags.models import Tag


class TestCreateJobForm(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="employer@gmail.com",
            password="123456",
            role="employer",
            first_name="John",
            last_name="Doe",
        )
        self.company = Company.objects.create(user=self.user, name="Dev Soft")
        self.category = Category.objects.create(
            name="Web Development",
            description="Web development roles",
        )
        self.valid_job = {
            "title": "Junior Software Engineer",
            "description": "Looking for Python developer",
            "vacancy": 2,
            "salary": 35000,
            "location": "Dhaka, Bangladesh",
            "type": "1",
            "category": self.category.id,
            "company": self.company.id,
            "application_deadline": (timezone.now() + timedelta(days=30)).date(),
            "workplace_type": "on_site",
            "experience_level": "entry",
            "status": "published",
            "salary_currency": "BDT",
            "salary_period": "month",
            "tags": [Tag.objects.create(name="Development").id],
        }

    def test_valid_and_save_form(self):
        form = CreateJobForm(data=self.valid_job)
        self.assertTrue(form.is_valid(), form.errors)

        job = form.save(commit=False)
        job.user = self.user
        job.save()
        for tag in form.cleaned_data["tags"]:
            job.tags.add(tag)

        self.assertIsInstance(job, Job)
        self.assertEqual(job.category_id, self.category.id)
        self.assertEqual(job.company_id, self.company.id)

    def test_field_required(self):
        form = CreateJobForm(data={})
        form.is_valid()

        self.assertEqual(form.errors["title"], ["This field is required."])
        self.assertEqual(form.errors["category"], ["This field is required."])
        self.assertEqual(form.errors["company"], ["This field is required."])
