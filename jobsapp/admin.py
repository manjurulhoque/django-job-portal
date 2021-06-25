from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

# Register your models here.
from jobsapp.models import Job


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
