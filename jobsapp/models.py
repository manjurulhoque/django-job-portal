# DJANGO Imports
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

# APP Imports
from accounts.models import User
from notifications.decorators import event_dispatcher
from notifications.events import EVENT_NEW_JOB

# Global Imports


@event_dispatcher(EVENT_NEW_JOB)
class Job(models.Model):
    JOB_TYPE_FULL_TIME = "1"
    JOB_TYPE_PART_TIME = "2"
    JOB_TYPE_INTERNSHIP = "3"
    JOB_TYPES = (
        (JOB_TYPE_FULL_TIME, _("Full time")),
        (JOB_TYPE_PART_TIME, _("Part time")),
        (JOB_TYPE_INTERNSHIP, _("Internship")),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User who creates this job."),
    )
    title = models.CharField(
        max_length=300, verbose_name=_("Title"), help_text=_("Short job title.")
    )
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Long job description.")
    )
    location = models.CharField(
        max_length=150, verbose_name=_("Location"), help_text=_("Location for this job position.")
    )
    type = models.CharField(
        choices=JOB_TYPES, max_length=10, verbose_name=_("Type"), help_text=_("Job type.")
    )
    category = models.CharField(
        max_length=100, verbose_name=_("Category"), help_text=_("Category clasification.")
    )
    last_date = models.DateTimeField(verbose_name=_("Last date"), help_text=_("Last date."))
    company_name = models.CharField(
        max_length=100, verbose_name=_("Company"), help_text=_("Job's Company name.")
    )
    company_description = models.CharField(
        max_length=300,
        verbose_name=_("Company description"),
        help_text=_("Company description, activity,..."),
    )
    website = models.CharField(
        max_length=100, default="", verbose_name=_("Website"), help_text=_("Company Website URL.")
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Created"), help_text=_("Job creation date and time.")
    )
    filled = models.BooleanField(
        default=False, verbose_name=_("Filled"), help_text=_("Job position is filled.")
    )
    salary = models.IntegerField(
        default=0, blank=True, verbose_name=_("Salary"), help_text=_("Maximum salary for this job.")
    )

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    def __str__(self) -> str:
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("User"), help_text=_("User applicant.")
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applicants",
        verbose_name=_("Job"),
        help_text=_("Job in applicant."),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Created"),
        help_text=_("Applicant creation date and time."),
    )

    class Meta:
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")
        unique_together = ("user", "job")

    def __str__(self) -> str:
        return self.user.get_full_name()
