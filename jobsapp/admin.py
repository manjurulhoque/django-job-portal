from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

# Register your models here.
from jobsapp.models import Job, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "industry",
        "size",
        "featured",
        "created_at",
    ]
    list_filter = ["featured", "industry", "size", "created_at"]
    search_fields = ["name", "industry", "description"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("user", "name", "description", "website")}),
        ("Branding", {"fields": ("logo",)}),
        ("Company Details", {"fields": ("industry", "size", "culture_benefits")}),
        ("Settings", {"fields": ("featured",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "salary",
        "location",
        "type",
        "category",
        "company",
        "company_name",
        "last_date",
        "created_at",
        "filled",
        "user",
    ]
    list_filter = ["salary", "last_date", "created_at", "user", "filled"]
    date_hierarchy = "created_at"
    search_fields = ["title", "company_name", "company__name"]
