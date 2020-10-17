from django.contrib import admin  # type: ignore

# Register your models here.
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "date_joined",
    ]
    list_filter = ["role", "is_active", "is_staff", "is_superuser"]
    fields = [
        "email",
        "first_name",
        "last_name",
        "gender",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    ]
