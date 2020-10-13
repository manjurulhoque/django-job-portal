from django.db import models
from django.utils import timezone

from accounts.models import User


class Job(models.Model):
    JOB_TYPE_FULL_TIME = "1"
    JOB_TYPE_PART_TIME = "2"
    JOB_TYPE_INTERNSHIP = "3"
    JOB_TYPES = (
        (JOB_TYPE_FULL_TIME, "Full time"),
        (JOB_TYPE_PART_TIME, "Part time"),
        (JOB_TYPE_INTERNSHIP, "Internship"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPES, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return self.user.get_full_name()
