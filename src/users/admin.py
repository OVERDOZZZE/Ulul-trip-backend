from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email", "username", "name", "is_verified","img_preview")
    list_display_links = ("email",)
    search_fields = ("email", "username")
    prepopulated_fields = {'user_slug': ('username',)}
    view_on_site = False
    fields = (
        "email",
        "username",
        "name",
        "number",
        "is_superuser",
        "is_verified",
        "is_active",
        "is_staff",
        "preview",
        "image",
        "user_slug",
        "password",
    )

    readonly_fields = ('is_verified','preview','password')

    def preview(self, obj):
        return mark_safe(f'<img src = "{obj.image.url}" style=height:200px />')


admin.site.register(User, UserAdmin)
