"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# if choose to change django language .. anywhere you translate
from django.utils.translation import gettext_lazy


from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = [
        # title, fields...
        (None, {"fields": ("email", "password")}),
        (
            gettext_lazy("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            gettext_lazy("Important dates"),
            {
                "fields": ("last_login",),
            },
        ),
    ]
    readonly_fields = ["last_login"]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    ]


# use our userAdmin to register the user model we defined in core.models
admin.site.register(models.User, UserAdmin)
