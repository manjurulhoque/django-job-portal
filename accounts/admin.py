from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    list_per_page = 20
    list_max_show_all = 100
    list_display_links = ["email"]
    list_select_related = []
