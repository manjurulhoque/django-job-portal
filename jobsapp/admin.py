from django.contrib import admin  # noqa

# Register your models here.
from jobsapp.models import Applicant, Job


class ApplicantInline(admin.TabularInline):
    model = Applicant
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "salary",
        "location",
        "type",
        "category",
        "company_name",
        "last_date",
        "created_at",
        "filled",
        "user",
    ]
    list_filter = ["salary", "last_date", "created_at", "user"]
    date_hierarchy = "created_at"
    inlines = [ApplicantInline]


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ["user", "job", "created_at"]
    list_filter = ["user", "created_at"]
    date_hierarchy = "created_at"
