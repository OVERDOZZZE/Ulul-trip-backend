from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_verified")
    list_display_links = ("email",)
    search_fields = ("email", "first_name")
    view_on_site = False
    fields = (
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_verified",
        "is_active",
        "is_staff",
        "password",
    )

    readonly_fields = ("is_verified", "password")


admin.site.register(User, UserAdmin)
