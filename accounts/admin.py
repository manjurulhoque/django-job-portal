from django.contrib import admin  # noqa

# Register your models here.
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
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
    list_filter = ["role", "gender", "is_active", "is_staff", "is_superuser"]
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


admin.site.register(User, UserAdmin)
