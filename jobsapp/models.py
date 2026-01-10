from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from tags.models import Tag

from .manager import JobManager


class JobType(models.TextChoices):
    FULL_TIME = "1", "Full time"
    PART_TIME = "2", "Part time"
    INTERNSHIP = "3", "Internship"


class CompanySize(models.TextChoices):
    SIZE_1_10 = "1", "1-10 employees"
    SIZE_11_50 = "2", "11-50 employees"
    SIZE_51_200 = "3", "51-200 employees"
    SIZE_201_500 = "4", "201-500 employees"
    SIZE_501_1000 = "5", "501-1000 employees"
    SIZE_1000_PLUS = "6", "1000+ employees"


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    website = models.URLField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(choices=CompanySize.choices, max_length=20, blank=True)
    culture_benefits = models.TextField(blank=True, help_text="Describe company culture, benefits, and perks")
    featured = models.BooleanField(default=False, help_text="Feature this company on the homepage")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["-featured", "-created_at"]

    def get_absolute_url(self):
        return reverse("jobs:company-detail", args=[self.id])

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JobType.choices, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100, blank=True, help_text="Legacy field - use company if available")
    company_description = models.CharField(max_length=300, blank=True, help_text="Legacy field - use company if available")
    website = models.CharField(max_length=100, default="", blank=True, help_text="Legacy field - use company if available")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)
    tags = models.ManyToManyField(Tag)
    vacancy = models.IntegerField(default=1)

    @property
    def display_company_name(self):
        """Return company name from Company model or fallback to legacy field"""
        return self.company.name if self.company else self.company_name

    @property
    def display_company_description(self):
        """Return company description from Company model or fallback to legacy field"""
        return self.company.description if self.company else self.company_description

    @property
    def display_company_website(self):
        """Return company website from Company model or fallback to legacy field"""
        return self.company.website if self.company else self.website

    @property
    def display_company_logo(self):
        """Return company logo if available"""
        return self.company.logo if self.company and self.company.logo else None

    objects = JobManager()

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.id])

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["id"]
        unique_together = ["user", "job"]

    def __str__(self):
        return self.user.get_full_name()

    @property
    def get_status(self):
        if self.status == 1:
            return "Pending"
        elif self.status == 2:
            return "Accepted"
        else:
            return "Rejected"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.job.title
