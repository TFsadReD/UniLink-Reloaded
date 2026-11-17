from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UniLinkUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("UniLink", {"fields": ("display_name",)}),
    )
    list_display = (
        "username",
        "display_name",
        "email",
        "is_staff",
        "is_active",
    )
