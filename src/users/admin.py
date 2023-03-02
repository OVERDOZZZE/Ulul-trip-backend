from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email", "username", "name", "is_verified","img_preview")
    list_display_links = ("email",)
    search_fields = ("email", "username")
    prepopulated_fields = {'user_slug': ('username',)}
    view_on_site = False

    readonly_fields = ('is_verified','preview')

    def preview(self, obj):
        return mark_safe(f'<img src = "{obj.image.url}" style=height:200px />')


admin.site.register(User, UserAdmin)
